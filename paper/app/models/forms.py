from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    """登录表单"""
    staff_id = StringField('工号', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class UserForm(FlaskForm):
    """用户表单"""
    staff_id = StringField('工号', validators=[DataRequired(), Length(1, 20)])
    name = StringField('姓名', validators=[DataRequired(), Length(1, 50)])
    gender = SelectField('性别', choices=[('男', '男'), ('女', '女')], validators=[DataRequired()])
    department = StringField('所在教研室', validators=[DataRequired(), Length(1, 50)])
    position = StringField('职务', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('密码', validators=[Length(6, 20)])
    password2 = PasswordField('确认密码', validators=[EqualTo('password')])
    role = SelectField('角色', choices=[('admin', '管理员'), ('teacher', '教师')], validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_staff_id(self, field):
        """验证工号是否已存在"""
        user = User.query.filter_by(staff_id=field.data).first()
        if user and user.id != self.id.data:
            raise ValidationError('该工号已被使用')


class PaperForm(FlaskForm):
    """试卷表单"""
    semester = StringField('所属学期', validators=[DataRequired(), Length(1, 20)])
    course_name = StringField('课程名称', validators=[DataRequired(), Length(1, 100)])
    class_name = StringField('班级', validators=[DataRequired(), Length(1, 50)])
    count = IntegerField('份数', validators=[DataRequired()])
    exam_type = SelectField('考试类型', choices=[('考试', '考试'), ('考查', '考查')], validators=[DataRequired()])
    storage_location = StringField('储存位置', validators=[Length(0, 100)])
    pdf_file = FileField('PDF文件', validators=[FileAllowed(['pdf'], '只允许上传PDF文件')])
    submit = SubmitField('提交')


class BorrowForm(FlaskForm):
    """借阅表单"""
    semester = StringField('所属学期', validators=[DataRequired(), Length(1, 20)])
    course_name = StringField('课程名称', validators=[DataRequired(), Length(1, 100)])
    class_name = StringField('班级', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField('借阅')


class ReturnForm(FlaskForm):
    """归还表单"""
    semester = StringField('所属学期', validators=[DataRequired(), Length(1, 20)])
    course_name = StringField('课程名称', validators=[DataRequired(), Length(1, 100)])
    class_name = StringField('班级', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField('归还')


class SearchForm(FlaskForm):
    """查询表单"""
    semester = StringField('所属学期')
    course_name = StringField('课程名称')
    class_name = StringField('班级')
    teacher_name = StringField('教师姓名')
    exam_type = SelectField('考试类型', choices=[('', '全部'), ('考试', '考试'), ('考查', '考查')])
    archived = SelectField('归档状态', choices=[('', '全部'), ('1', '已归档'), ('0', '未归档')])
    submit = SubmitField('查询') 