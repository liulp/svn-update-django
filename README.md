# svn-update-django 文件更新django版
自己用django写的从测试到生产环境的，基于svn的文件或文件夹更新


本代码适用于PHP代码，这是第一个版本，只做功能，代码写的很low，仅供参考。windows ，linux 通用，但是windows 未做回滚功能。

总共用到了6张数据表， 
login_user：用户登录表
update_host: 主机表。记录更新主机信息表（帐号密码端口） ssh（linux） 或ftp（windows）
update_project：项目表。主要是记录项目名称，项目svn地址， 项目本地文件夹的地址，以及要更新文件的前缀（最多2个）
update_prohost: 主机项目关系表。不同主机不同项目的目标地址
update_entry:历史更新记录表（备份文件放在/opt/backup）
update_rollback：历史回滚记录表

本人邮箱89032338@qq.com


