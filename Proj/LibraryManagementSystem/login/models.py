from django.db import models

# Create your models here.


class UserInfo(models.Model):
    """用户类"""
    user_account = models.CharField(max_length=12)
    user_password = models.CharField(max_length=40)
    user_age = models.IntegerField()
    user_sex = models.CharField(max_length=10)
    user_phone = models.CharField(max_length=12)

    def __str__(self):
        return self.user_account

    class Meta:
        db_table = "user_info"

    def account(self):
        return self.user_account

    def password(self):
        return self.user_password

    def age(self):
        return self.user_age

    def sex(self):
        return self.user_sex

    def phone(self):
        return self.user_phone

    account.short_description = "账号"
    password.short_description = "密码"
    age.short_description = "年龄"
    sex.short_description = "性别"
    phone.short_description = "手机号"


class BookInfo(models.Model):
    """图书类"""
    ISBN = models.CharField(max_length=12, primary_key=True)
    book_name = models.CharField(max_length=40)
    book_author = models.CharField(max_length=20)
    book_publish = models.CharField(max_length=20)
    publication_date = models.DateTimeField()
    book_num = models.IntegerField()

    def __str__(self):
        return self.ISBN

    class Meta:
        db_table = "book_info"

    def isbn(self):
        return self.ISBN

    def name(self):
        return self.book_name

    def author(self):
        return self.book_author

    def publish(self):
        return self.book_publish

    def date(self):
        return self.publication_date

    def num(self):
        return self.book_num

    isbn.short_description = "书籍编号"
    name.short_description = "书籍名称"
    author.short_description = "书籍作者"
    publish.short_description = "书籍出版社"
    date.short_description = "书籍出版日期"
    num.short_description = "在馆数量"


class BorrowInfo(models.Model):
    """借阅信息类"""
    borrower_id = models.ForeignKey('UserInfo')
    book_id = models.ForeignKey('BookInfo')
    borrowing_time = models.DateTimeField()
    return_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{0},{1}".format(self.borrower_id.user_account, self.book_id.book_name)

    class Meta:
        db_table = "borrow_info"

    def borrower(self):
        return self.borrower_id

    def book(self):
        return self.book_id

    def borrowing(self):
        return self.borrowing_time

    def return_(self):
        return self.return_time

    borrower.short_description = "借阅者id"
    book.short_description = "书籍编号"
    borrowing.short_description = "借阅时间"
    return_.short_description = "归还时间"
