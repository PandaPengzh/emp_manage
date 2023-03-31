"""
自定义分页组件
"""
import math
from django.utils.safestring import mark_safe

class Pagination(object):

    def __init__(self,request,queryset,page_size=20,plus=3):
        # 截获关于page的请求
        page = int(request.GET.get('page','1'))
        self.page = page    # 获取到的页面数
        self.page_size = page_size # 每页多少条
        self.start_page = (page-1) * page_size     # 起始页
        self.end_page = page_size * page # 终止页

        # 计算应该生成多少分页标签
        self.total_count = queryset.count()   # 数据库中总条数
        self.total_page_count = math.ceil(self.total_count/page_size)    # ceil 向上取整

        self.queryset = queryset[self.start_page:self.end_page]     # 分页

        self.plus = plus     # 只想显示当前页的前三页、后三页
  
    
    def html_data(self):
        page_str_list = []    # 保存让前端生成的代码

        # 首页
        first_page = """
            <li>
                <a href="?page={}" aria-label="Previous">
                    <span aria-hidden="true">首页</span>
                </a>
            </li>
            """.format(1)
        page_str_list.append(first_page)

        # 前一页
        if self.page >=2:
            back_page = """
            <li>
                <a href="?page={}" aria-label="Previous">
                    <span aria-hidden="true">上一页</span>
                </a>
            </li>
            """.format(self.page-1)
            page_str_list.append(back_page)

    

        start_num = self.page - self.plus
        end_num = self.page + self.plus

        # 对极值的限制
        if self.total_page_count <= 2*self.plus +1:  # 当数据库中的数据少于7页时
            start_num = 1
            end_num = self.total_page_count
        else:
            # 遇见极小值时
            if self.page <= self.plus:
                start_num = 1
                end_num = 2 * self.plus + 1
            # 遇见极大值
            else:
                if (self.page+self.plus) >= self.total_page_count:
                    start_num = self.total_page_count - 2 * self.plus
                    end_num = self.total_page_count -1
                    

        for i in range(start_num,end_num+1):
            if i == self.page:
                page_string = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)  # 添加样式
            else:
                page_string = '<li><a href="?page={}">{}</a></li>'.format(i,i)
            page_str_list.append(page_string)


        # 后一页
        if self.page <= self.total_page_count-2:
            prv_page = """
            <li>
                <a href="?page={}" aria-label="Previous">
                    <span aria-hidden="true">下一页</span>
                </a>
            </li>
            """.format(self.page+1)
            page_str_list.append(prv_page)

        # 尾页
        last_page = """
            <li>
                <a href="?page={}" aria-label="Previous">
                    <span aria-hidden="true">尾页</span>
                </a>
            </li>
            """.format(self.total_page_count-1)
        page_str_list.append(last_page)

        return mark_safe("".join(page_str_list))