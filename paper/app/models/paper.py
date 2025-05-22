from datetime import datetime
from app import db

class Paper(db.Model):
    """试卷信息表"""
    __tablename__ = 'papers'

    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(20), nullable=False, comment='所属学期')
    course_name = db.Column(db.String(100), nullable=False, comment='试卷名称/课程名称')
    class_name = db.Column(db.String(50), nullable=False, comment='班级')
    count = db.Column(db.Integer, nullable=False, comment='份数')
    exam_type = db.Column(db.String(20), nullable=False, comment='考试或考查')
    storage_location = db.Column(db.String(100), comment='纸质试卷储存位置')
    pdf_path = db.Column(db.String(255), comment='PDF文件路径')
    archived = db.Column(db.Boolean, default=False, comment='是否已归档')
    archive_date = db.Column(db.DateTime, comment='归档日期')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    borrowings = db.relationship('Borrowing', backref='paper', lazy='dynamic')

    def __repr__(self):
        return f'<Paper {self.course_name} - {self.class_name}>'


class Borrowing(db.Model):
    """调阅信息表"""
    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment='借阅日期')
    return_date = db.Column(db.DateTime, comment='归还日期')
    status = db.Column(db.String(20), default='borrowed', comment='状态：borrowed/returned')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Borrowing {self.id}>' 