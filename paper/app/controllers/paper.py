import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
import matplotlib.pyplot as plt
import io
import base64

from app import db
from app.models.paper import Paper, Borrowing
from app.models.user import User
from app.models.forms import PaperForm, BorrowForm, ReturnForm, SearchForm
from app.utils.permissions import admin_required

# 创建蓝图
paper_bp = Blueprint('paper', __name__)


@paper_bp.route('/')
@login_required
def index():
    """首页"""
    # 统计已归档和未归档试卷数量
    total_papers = Paper.query.count()
    archived_papers = Paper.query.filter_by(archived=True).count()
    unarchived_papers = total_papers - archived_papers
    
    # 绘制饼图
    if total_papers > 0:
        fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))
        labels = ['已归档', '未归档']
        sizes = [archived_papers, unarchived_papers]
        colors = ['#ff9999', '#66b3ff']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # 保存图片到内存中
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close(fig)
    else:
        plot_url = None
    
    # 最近的试卷
    recent_papers = Paper.query.order_by(Paper.created_at.desc()).limit(5).all()
    
    # 最近的借阅
    recent_borrowings = Borrowing.query.filter_by(status='borrowed').order_by(Borrowing.borrow_date.desc()).limit(5).all()
    
    return render_template('paper/index.html', 
                          total_papers=total_papers,
                          archived_papers=archived_papers,
                          unarchived_papers=unarchived_papers,
                          recent_papers=recent_papers,
                          recent_borrowings=recent_borrowings,
                          plot_url=plot_url)


@paper_bp.route('/papers')
@login_required
def papers():
    """试卷列表"""
    form = SearchForm(request.args)
    query = Paper.query
    
    if form.semester.data:
        query = query.filter(Paper.semester.like(f'%{form.semester.data}%'))
    if form.course_name.data:
        query = query.filter(Paper.course_name.like(f'%{form.course_name.data}%'))
    if form.class_name.data:
        query = query.filter(Paper.class_name.like(f'%{form.class_name.data}%'))
    if form.teacher_name.data:
        query = query.join(User).filter(User.name.like(f'%{form.teacher_name.data}%'))
    if form.exam_type.data:
        query = query.filter(Paper.exam_type == form.exam_type.data)
    if form.archived.data:
        archived = form.archived.data == '1'
        query = query.filter(Paper.archived == archived)
    
    papers = query.order_by(Paper.created_at.desc()).all()
    
    return render_template('paper/papers.html', papers=papers, form=form)


@paper_bp.route('/papers/new', methods=['GET', 'POST'])
@login_required
def new_paper():
    """新建试卷"""
    form = PaperForm()
    if form.validate_on_submit():
        pdf_path = None
        if form.pdf_file.data:
            pdf_file = form.pdf_file.data
            filename = f"{form.semester.data}_{form.course_name.data}_{form.class_name.data}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf_path = os.path.join('uploads', filename)
            pdf_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        paper = Paper(
            semester=form.semester.data,
            course_name=form.course_name.data,
            class_name=form.class_name.data,
            count=form.count.data,
            exam_type=form.exam_type.data,
            storage_location=form.storage_location.data,
            pdf_path=pdf_path,
            archived=True,
            archive_date=datetime.utcnow(),
            teacher_id=current_user.id
        )
        
        db.session.add(paper)
        db.session.commit()
        flash('试卷提交成功', 'success')
        return redirect(url_for('paper.papers'))
    
    return render_template('paper/paper_form.html', form=form, title='新建试卷')


@paper_bp.route('/papers/<int:id>')
@login_required
def paper_detail(id):
    """试卷详情"""
    paper = Paper.query.get_or_404(id)
    borrowings = Borrowing.query.filter_by(paper_id=id).order_by(Borrowing.borrow_date.desc()).all()
    
    return render_template('paper/paper_detail.html', paper=paper, borrowings=borrowings)


@paper_bp.route('/papers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_paper(id):
    """编辑试卷"""
    paper = Paper.query.get_or_404(id)
    
    # 检查权限
    if not current_user.is_admin() and paper.teacher_id != current_user.id:
        abort(403)
    
    form = PaperForm(obj=paper)
    if form.validate_on_submit():
        pdf_path = paper.pdf_path
        if form.pdf_file.data:
            # 如果上传了新文件，则删除旧文件
            if pdf_path:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(pdf_path))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            pdf_file = form.pdf_file.data
            filename = f"{form.semester.data}_{form.course_name.data}_{form.class_name.data}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf_path = os.path.join('uploads', filename)
            pdf_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        paper.semester = form.semester.data
        paper.course_name = form.course_name.data
        paper.class_name = form.class_name.data
        paper.count = form.count.data
        paper.exam_type = form.exam_type.data
        paper.storage_location = form.storage_location.data
        paper.pdf_path = pdf_path
        
        db.session.commit()
        flash('试卷更新成功', 'success')
        return redirect(url_for('paper.paper_detail', id=paper.id))
    
    return render_template('paper/paper_form.html', form=form, paper=paper, title='编辑试卷')


@paper_bp.route('/papers/<int:id>/delete', methods=['POST'])
@login_required
def delete_paper(id):
    """删除试卷"""
    paper = Paper.query.get_or_404(id)
    
    # 检查权限
    if not current_user.is_admin() and paper.teacher_id != current_user.id:
        abort(403)
    
    # 删除文件
    if paper.pdf_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(paper.pdf_path))
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(paper)
    db.session.commit()
    flash('试卷删除成功', 'success')
    return redirect(url_for('paper.papers'))


@paper_bp.route('/papers/<int:id>/pdf')
@login_required
def view_pdf(id):
    """查看PDF文件"""
    paper = Paper.query.get_or_404(id)
    
    if not paper.pdf_path:
        flash('该试卷没有PDF文件', 'warning')
        return redirect(url_for('paper.paper_detail', id=id))
    
    filename = os.path.basename(paper.pdf_path)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@paper_bp.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    """借阅试卷"""
    form = BorrowForm()
    
    # 从数据库获取已归档试卷的学期、课程名称和班级列表作为下拉选项
    archived_papers = Paper.query.filter(Paper.archived == True).all()
    
    # 提取所有学期、课程、班级的唯一组合
    paper_data = {}
    semesters = []
    
    for paper in archived_papers:
        if paper.semester not in semesters:
            semesters.append(paper.semester)
            paper_data[paper.semester] = {}
            
        if paper.course_name not in paper_data[paper.semester]:
            paper_data[paper.semester][paper.course_name] = []
            
        if paper.class_name not in paper_data[paper.semester][paper.course_name]:
            paper_data[paper.semester][paper.course_name].append(paper.class_name)
    
    # 打印调试信息
    print(f"找到 {len(semesters)} 个学期选项: {', '.join(semesters)}")
    print(f"paper_data 结构: {paper_data}")
    
    # 设置学期选项
    form.semester.choices = [(s, s) for s in semesters]
    
    # 初始化其他下拉框
    if not semesters:
        form.course_name.choices = [('', '暂无课程')]
        form.class_name.choices = [('', '暂无班级')]
    else:
        form.course_name.choices = [('', '请选择学期')]
        form.class_name.choices = [('', '请选择课程')]
    
    # 如果是AJAX请求，不处理
    if request.args.get('_') or request.args.get('semester') or request.args.get('course_name'):
        return render_template('paper/borrow_form.html', form=form, paper_data=paper_data)
    
    # 如果是POST请求，在验证表单之前根据学期和课程动态更新选项列表
    if request.method == 'POST':
        selected_semester = request.form.get('semester', '')
        selected_course = request.form.get('course_name', '')
        
        print(f"表单提交 - 选择的学期: {selected_semester}, 课程: {selected_course}")
        
        # 更新课程选项
        if selected_semester and selected_semester in paper_data:
            form.course_name.choices = [('', '请选择课程')] + [(c, c) for c in paper_data[selected_semester].keys()]
            
            # 更新班级选项
            if selected_course and selected_course in paper_data[selected_semester]:
                form.class_name.choices = [('', '请选择班级')] + [(c, c) for c in paper_data[selected_semester][selected_course]]
    
    if form.validate_on_submit():
        # 查找对应试卷
        paper = Paper.query.filter(
            Paper.semester == form.semester.data,
            Paper.course_name == form.course_name.data,
            Paper.class_name == form.class_name.data,
            Paper.archived == True
        ).first()
        
        if not paper:
            flash('未找到对应的已归档试卷', 'danger')
            return render_template('paper/borrow_form.html', form=form, paper_data=paper_data)
        
        # 检查是否已借阅
        existing_borrow = Borrowing.query.filter(
            Borrowing.paper_id == paper.id,
            Borrowing.borrower_id == current_user.id,
            Borrowing.status == 'borrowed'
        ).first()
        
        if existing_borrow:
            flash('您已经借阅了该试卷', 'warning')
            return redirect(url_for('paper.paper_detail', id=paper.id))
        
        # 创建借阅记录
        borrowing = Borrowing(
            paper_id=paper.id,
            borrower_id=current_user.id,
            borrow_date=datetime.utcnow(),
            status='borrowed'
        )
        
        db.session.add(borrowing)
        db.session.commit()
        flash('试卷借阅成功', 'success')
        return redirect(url_for('paper.paper_detail', id=paper.id))
    
    return render_template('paper/borrow_form.html', form=form, paper_data=paper_data)


@paper_bp.route('/return', methods=['GET', 'POST'])
@login_required
def return_paper():
    """归还试卷"""
    form = ReturnForm()
    
    # 获取当前用户已借阅但未归还的试卷信息
    borrowed_papers = db.session.query(Paper).join(Borrowing).filter(
        Borrowing.borrower_id == current_user.id,
        Borrowing.status == 'borrowed'
    ).all()
    
    # 提取所有学期、课程、班级的唯一组合
    paper_data = {}
    semesters = []
    
    for paper in borrowed_papers:
        if paper.semester not in semesters:
            semesters.append(paper.semester)
            paper_data[paper.semester] = {}
            
        if paper.course_name not in paper_data[paper.semester]:
            paper_data[paper.semester][paper.course_name] = []
            
        if paper.class_name not in paper_data[paper.semester][paper.course_name]:
            paper_data[paper.semester][paper.course_name].append(paper.class_name)
    
    # 打印调试信息
    print(f"归还功能找到 {len(semesters)} 个学期选项: {', '.join(semesters)}")
    print(f"归还功能 paper_data 结构: {paper_data}")
    
    # 设置学期选项
    form.semester.choices = [(s, s) for s in semesters]
    
    # 初始化其他下拉框
    if not semesters:
        form.course_name.choices = [('', '暂无课程')]
        form.class_name.choices = [('', '暂无班级')]
    else:
        form.course_name.choices = [('', '请选择学期')]
        form.class_name.choices = [('', '请选择课程')]
    
    # 如果是AJAX请求，不处理
    if request.args.get('_') or request.args.get('semester') or request.args.get('course_name'):
        return render_template('paper/return_form.html', form=form, paper_data=paper_data)
    
    # 如果是POST请求，在验证表单之前根据学期和课程动态更新选项列表
    if request.method == 'POST':
        selected_semester = request.form.get('semester', '')
        selected_course = request.form.get('course_name', '')
        selected_class = request.form.get('class_name', '')
        
        # 也获取隐藏字段的值作为备份
        hidden_semester = request.form.get('selected_semester', '')
        hidden_course = request.form.get('selected_course', '')
        hidden_class = request.form.get('selected_class', '')
        
        print(f"归还表单提交 - 选择的学期: {selected_semester}/{hidden_semester}, 课程: {selected_course}/{hidden_course}, 班级: {selected_class}/{hidden_class}")
        
        # 更新课程选项（优先使用下拉框的值，如果没有则使用隐藏字段的值）
        effective_semester = selected_semester or hidden_semester
        effective_course = selected_course or hidden_course
        
        if effective_semester and effective_semester in paper_data:
            form.course_name.choices = [('', '请选择课程')] + [(c, c) for c in paper_data[effective_semester].keys()]
            
            # 更新班级选项
            if effective_course and effective_course in paper_data[effective_semester]:
                form.class_name.choices = [('', '请选择班级')] + [(c, c) for c in paper_data[effective_semester][effective_course]]
    
    if form.validate_on_submit():
        # 查找对应试卷
        paper = Paper.query.filter(
            Paper.semester == form.semester.data,
            Paper.course_name == form.course_name.data,
            Paper.class_name == form.class_name.data
        ).first()
        
        if not paper:
            flash('未找到对应的试卷', 'danger')
            return render_template('paper/return_form.html', form=form, paper_data=paper_data)
        
        # 查找借阅记录
        borrowing = Borrowing.query.filter(
            Borrowing.paper_id == paper.id,
            Borrowing.borrower_id == current_user.id,
            Borrowing.status == 'borrowed'
        ).first()
        
        if not borrowing:
            flash('未找到您的借阅记录', 'warning')
            return render_template('paper/return_form.html', form=form, paper_data=paper_data)
        
        # 更新借阅记录
        borrowing.return_date = datetime.utcnow()
        borrowing.status = 'returned'
        
        db.session.commit()
        flash('试卷归还成功', 'success')
        return redirect(url_for('paper.paper_detail', id=paper.id))
    
    return render_template('paper/return_form.html', form=form, paper_data=paper_data)


@paper_bp.route('/borrowings')
@login_required
def borrowings():
    """借阅记录"""
    if current_user.is_admin():
        # 管理员可以查看所有借阅记录
        borrowings = Borrowing.query.order_by(Borrowing.borrow_date.desc()).all()
    else:
        # 普通用户只能查看自己的借阅记录
        borrowings = Borrowing.query.filter_by(borrower_id=current_user.id).order_by(Borrowing.borrow_date.desc()).all()
    
    return render_template('paper/borrowings.html', borrowings=borrowings)


@paper_bp.route('/statistics')
@login_required
def statistics():
    """统计信息"""
    # 统计已归档和未归档试卷数量
    total_papers = Paper.query.count()
    archived_papers = Paper.query.filter_by(archived=True).count()
    unarchived_papers = total_papers - archived_papers
    
    # 统计考试类型
    exam_papers = Paper.query.filter_by(exam_type='考试').count()
    check_papers = Paper.query.filter_by(exam_type='考查').count()
    
    # 统计每月归档数量 - 使用MySQL的DATE_FORMAT代替SQLite的strftime
    monthly_stats = db.session.query(
        db.func.DATE_FORMAT(Paper.archive_date, '%Y-%m').label('month'),
        db.func.count(Paper.id).label('count')
    ).filter(Paper.archived == True).group_by('month').order_by('month').all()
    
    months = [stat[0] for stat in monthly_stats] if monthly_stats else []
    counts = [stat[1] for stat in monthly_stats] if monthly_stats else []
    
    # 绘制饼图 - 归档状态
    fig1, ax1 = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))
    labels1 = ['已归档', '未归档']
    sizes1 = [archived_papers, unarchived_papers]
    colors1 = ['#ff9999', '#66b3ff']
    
    if total_papers > 0:
        ax1.pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
        plt.close(fig1)
    else:
        plot_url1 = None
    
    # 绘制饼图 - 考试类型
    fig2, ax2 = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))
    labels2 = ['考试', '考查']
    sizes2 = [exam_papers, check_papers]
    colors2 = ['#c2c2f0', '#ffcc99']
    
    if total_papers > 0:
        ax2.pie(sizes2, labels=labels2, colors=colors2, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
        plt.close(fig2)
    else:
        plot_url2 = None
    
    # 绘制柱状图 - 每月归档数量
    if months:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.bar(months, counts, color='#5d88f0')
        ax3.set_xlabel('月份')
        ax3.set_ylabel('归档数量')
        ax3.set_title('每月试卷归档数量')
        plt.xticks(rotation=45)
        
        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        plot_url3 = base64.b64encode(img3.getvalue()).decode('utf8')
        plt.close(fig3)
    else:
        plot_url3 = None
    
    return render_template('paper/statistics.html',
                          total_papers=total_papers,
                          archived_papers=archived_papers,
                          unarchived_papers=unarchived_papers,
                          exam_papers=exam_papers,
                          check_papers=check_papers,
                          plot_url1=plot_url1,
                          plot_url2=plot_url2,
                          plot_url3=plot_url3,
                          months=months,
                          counts=counts) 