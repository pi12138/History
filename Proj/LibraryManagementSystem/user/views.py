from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from login.views import encrypt_md5
# Create your views here.


def user_info(request):
    """用户主页"""
    user_name = request.session.get("user_account", None)

    if user_name is None:
        return render(request, 'login/login.html')
    else:
        context = {
            "user_name": user_name,
        }
        return render(request, "user/user_info.html", context)


def inquire(request):
    """查询已借阅书籍"""

    user_account = request.session['user_account']

    try:
        user = UserInfo.objects.get(user_account=user_account)
        borrow_list = BorrowInfo.objects.filter(borrower_id=user.id)
        book_num = len(borrow_list)
        borrow_list = reversed(borrow_list)

        book_list = []
        not_return = 0

        for borrow in borrow_list:
            book_info = {}

            book = BookInfo.objects.get(ISBN=borrow.book_id)

            book_info['ISBN'] = book.ISBN
            book_info['book_name'] = book.book_name
            book_info['book_author'] = book.book_author
            book_info['borrowing_time'] = borrow.borrowing_time

            if borrow.return_time is None:
                book_info['return_time'] = "未归还"
                not_return += 1
            else:
                book_info['return_time'] = borrow.return_time

            book_list.append(book_info)

        context = {
            "user_name": user_account,
            "book_num": book_num,
            "book_list": book_list,
            "not_return": not_return,
        }

        # return render(request, "user/user_info.html", context)
        return render(request, "user/inquire.html", context)

    except Exception as e:
        # return render(request, "user/user_info.html")
        return HttpResponse("e:", e)


def books_list(request, page_index):
    """图书列表"""
    books = BookInfo.objects.all()

    if page_index == "":
        page_index = 1

    # 分页
    paginator = Paginator(books, 2)

    page = paginator.page(page_index)

    context = {
        "user_name": request.session['user_account'],
        "books": books,
        "page": page,
        "page_range": paginator.page_range,
    }

    # return render(request, "user/user_info.html", context)
    return render(request, "user/book_list.html", context)


def search_books(request):
    """搜索书籍"""
    book_name = request.POST.get('book_name', None)

    try:
        found_book = BookInfo.objects.get(book_name=book_name)

        context = {
            "user_name": request.session['user_account'],
            "found_book": found_book,
        }

        # return render(request, "user/user_info.html", context)
        return render(request, "user/search_books.html", context)

    except Exception as e:
        return HttpResponse("search_books error:{}".format(e))


def borrowing_books(request):
    """借阅图书"""

    borrowing_book_isbn = request.POST['borrowing_book_ISBN']

    try:
        book = BookInfo.objects.get(ISBN=borrowing_book_isbn)

        borrow = BorrowInfo()
        borrow.book_id = BookInfo.objects.get(ISBN=borrowing_book_isbn)
        borrow.borrower_id = UserInfo.objects.get(user_account=request.session["user_account"])
        borrow.borrowing_time = get_time()
        borrow.save()

        book.book_num -= 1
        book.save()
        context = {
            "borrowing_result": "借阅成功！",
            "user_name": request.session['user_account'],
        }
        # return HttpResponse("借阅成功！")
        return render(request, 'user/user_info.html', context)

    except Exception as e:
        return HttpResponse("borrowing_books error:{}".format(e))


def returning_books(request):
    """还书"""

    isbn = request.POST['ISBN']
    user = request.session['user_account']

    try:
        book = BookInfo.objects.get(ISBN=isbn)
        borrow = BorrowInfo.objects.filter(book_id__ISBN=isbn).filter(borrower_id__user_account=user).filter(return_time=None).first()
        borrow.return_time = get_time()
        borrow.save()

        book.book_num += 1
        book.save()

        context = {
            "returning_result": "归还成功！",
            "user_name": request.session['user_account'],
        }
        # return HttpResponse("归还成功！")
        return render(request, "user/user_info.html", context)

    except Exception as e:
        return HttpResponse("returning_books error:{}".format(e))


def not_returned_books(request):
    """未归还书籍"""
    user_account = request.session['user_account']

    try:
        user = UserInfo.objects.get(user_account=user_account)

        not_returned_list = BorrowInfo.objects.filter(borrower_id=user.id).filter(return_time=None)

        not_return = 0
        not_returned = []

        for borrow in not_returned_list:
            book_info = {}

            book = BookInfo.objects.get(ISBN=borrow.book_id)
            book_info['ISBN'] = book.ISBN
            book_info['book_name'] = book.book_name
            book_info['book_author'] = book.book_author
            book_info['borrowing_time'] = borrow.borrowing_time

            if borrow.return_time is None:
                book_info['return_time'] = "未归还"
                not_return += 1
            else:
                book_info['return_time'] = borrow.return_time

            not_returned.append(book_info)

        context = {
            "not_returned_books": not_returned,
            "not_return": not_return,
            "user_name": user_account,
        }

        # return render(request, "user/user_info.html", context)
        return render(request, "user/not_returned_books.html", context)

    except Exception as e:
        return HttpResponse("not_returned_books error:{}".format(e))


def get_time():
    """获取当前时间，按照一定格式"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def alter_user_info(request):
    """修改用户信息操作"""
    account = request.session.get("user_account", None)

    if account is None:
        return HttpResponse("发生了未知异常！")
    else:
        try:
            user = UserInfo.objects.get(user_account=account)

            context = {
                "user_account": account,
                # "user_password": user.user_password,
                # "user_age": user.user_age,
                "user_sex": user.user_sex,
                # "user_phone": user.user_phone,
                "alter_result": ""
            }
        except Exception as e:
            return HttpResponse("alter_user_info error:{}".format(e))

    return render(request, "user/alter_user_info.html", context)


def alter_user_info_handle(request):
    """处理用户账户信息修改操作"""
    account = request.POST.get("user_account", None)

    if account is None:
        return HttpResponse("发生了未知的错误！")
    else:
        try:
            user = UserInfo.objects.get(user_account=account)

            # user.user_password = request.POST.get("user_password")
            password = request.POST.get("user_password")
            user.user_password = encrypt_md5(password)
            user.user_sex = request.POST.get("user_sex")
            user.user_age = request.POST.get("user_age")
            user.user_phone = request.POST.get("user_phone")
            user.save()

            context = {
                "user_account": user.user_account,
                # "user_password": user.user_password,
                "user_password": password,
                "user_age": user.user_age,
                "user_sex": user.user_sex,
                "user_phone": user.user_phone,
                "alter_result": True
            }

        except Exception as e:
            return HttpResponse("alter_user_info_handle error:{}".format(e))

        return render(request, "user/alter_user_info.html", context)


def delete_user_info(request):
    """删除账户页面"""
    account = request.session.get("user_account", None)

    if account is None:
        return HttpResponse("发生了未知的错误！")
    else:

        context = {"user_account": account}

    return render(request, "user/delete_user_info.html", context)


def delete_user_info_handle(request):
    """删除账户操作"""
    account = request.POST.get("user_account", None)

    if account is None:
        return HttpResponse("发生了未知的错误！")
    else:

        try:

            password = request.POST.get("user_password", None)
            password = encrypt_md5(password)
            phone = request.POST.get("user_phone", None)

            user = UserInfo.objects.get(user_account=account)
            user_password = user.user_password
            user_phone = user.user_phone

            if user_password == password and user_phone == phone:

                user.delete()

                context = {
                    "delete_result": True
                }
            else:
                return HttpResponse("密码或者手机号错误！")

        except Exception as e:
            return HttpResponse("delete_user_info_handle error:{}".format(e))

    request.session.flush()

    return render(request, 'user/delete_user_info.html', context)

