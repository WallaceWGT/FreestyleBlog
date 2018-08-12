"--wallace--"

class CustomPager(object):
    def __init__(self,totalCount,currentPage=1,perPagerItemNum=20,perPageNum=10):
        self.total_count = totalCount  #数据总个数
        self.current_Page = currentPage #当前页
        self.per_pager_item_num = perPagerItemNum #每页显示的数据行数
        self.per_page_num = perPageNum #每页码的个数
    #生成页面数据切片的首尾索引
    @property
    def start(self):
        return (self.current_Page-1)*self.per_page_num
    @property
    def end(self):
        return (self.current_Page)*self.per_page_num
    #求页面的总页数
    @property
    def total_page_num(self):
        #总页数
        page_num,another_page = divmod(self.total_count,self.per_pager_item_num)
        if another_page==0:
            return page_num
        return page_num+1
    #通过该方法生成每页码的数据
    @property
    def per_page_range(self):
        #总页数少的时候
        if self.total_page_num <= self.per_page_num:
            return range(1,self.total_page_num+1)
        #总页数多的时候
        half_page_num = int(self.per_page_num/2)
        #当前页小于页码的一般的时候
        if self.current_Page<=half_page_num:
            return range(1,self.per_page_num+1)
        #在最后那几页
        if self.current_Page+half_page_num>=self.total_page_num:
            return range(self.total_page_num-self.per_page_num+1,self.total_page_num+1)

        return range(self.current_Page-half_page_num,self.current_Page+half_page_num)
    #通过该页面生成页码标签
    @property
    def page_str(self):
        '''
        创建分页的页码标签
        :return:
        '''
        #页码标签的列表
        page_link_list=[]

        #页面标签的生成
        first_page = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">首页</a></li>'% 1
        page_link_list.append(first_page)
        if self.current_Page==1:
            first = '<li class="page-item"><a href="#" class="page-link">上一页</a></li>'
        else:
            first = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">上一页</a></li>'%(self.current_Page-1)
        page_link_list.append(first)
        #中间数字
        for page_link_num in self.per_page_range:
            if self.current_Page==page_link_num:
                temp = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">%s</a></li>' % (page_link_num,page_link_num)
            else:
                temp = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">%s</a></li>' % (page_link_num, page_link_num)
            page_link_list.append(temp)

        if self.current_Page==self.total_page_num:
            meddil = '<li class="page-item"><a href="#" class="page-link">下一页</a></li>'
        else:
            meddil = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">下一页</a></li>'%(self.current_Page+1,)
        page_link_list.append(meddil)

        last_page = '<li class="page-item"><a href="/mainBlog?p=%s" class="page-link">尾页</a></li>'%(self.total_page_num,)
        page_link_list.append(last_page)

        return page_link_list