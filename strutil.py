#coding=utf8
class StrUtil:
    # @staticmethod
    # def getcontenttype(content):
    #     lists = content.split()
    #     if len(lists) < 2:
    #         return u'content',''
    #     else:
    #         return lists[0],lists[1]
    @staticmethod
    def getcontenttype(content):
        lists = content.split()
        if len(lists) < 2:
            return u'content',''
        else:
            return lists[0],' '.join(lists[1:])

if __name__ == '__main__':
    #  s='a b  c d b dd  e'
    # s = 'abcd'
    # #  s.split()
    # lists = s.split()
    # print len(lists)
    # p = ','.join(s.split())
    # print p
    p,p1 = StrUtil.getcontenttype('a b  c c d')
    print p
    print p1
