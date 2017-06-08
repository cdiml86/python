import pymysql

def connDB(): #连接数据库函数
    conn=pymysql.connect(host='localhost',user='root',passwd='danailin',db='wechat',charset='utf8mb4')
    cur=conn.cursor();
    return (conn,cur);

def exeUpdate(cur,sql):#更新语句，可执行update,insert语句
    sta=cur.execute(sql);
    return(sta);

def exeDelete(cur,IDs): #删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta=cur.execute('delete from relationTriple where tID =%d'% int(eachID));
    return (sta);

def exeQuery(cur,sql):#查询语句
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.close();
    
#调用连接数据库的函数        
conn=connDB();
cur=connDB();

#调用更新记录的函数
sta=exeUpdate(cur, "INSERT INTO content_list(date_d,nick_name,contentd) values('2017-05-22','A','123')");
if(sta==1):
    print('插入成功');
else:
    print('插入失败');
    
#查询现有数据，并打印    
exeQuery(cur, "select * from list_name")  ;
for each in cur:
    print(each[0],each[1].decode('utf-8'));
    
# 批量删除记录，用户输入要删除的记录id号    
# tempID=input('请输入要删除的编号 编号之间用空格分开：');
# sta=exeDelete(cur, tempID);
# if(sta==1):
#     print('删除成功');
# else:
#     print('删除失败');

connClose(conn, cur);