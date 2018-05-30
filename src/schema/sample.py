# -*- coding: utf-8 -*-

from schema.Base import Base

# 数据库字符集应当使用 utf8mb4
# innodb引擎在的最长索引字节数为767Bytes，在utf8mb4字符集下折合字符长度为191字符
class TableSample(Base):
    def Name(self):
        return 'foobar'

    def Version(self):
        return 1

    def Schema(self):
        sql = '''
CREATE TABLE `{}` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(256) NOT NULL,
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '记录更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uniq_name` (`name`(128)),
    KEY `idx_create_time` (`create_time`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        '''.strip()
        return sql.format(
            self.Name()
        )

    # ver1 -> ver2, ver2 -> ver3
    # also
    # ver1 -> ver3

    #def Ver1_Ver2(self, cursor):
    #    return

    #def Ver2_Ver3(self, cursor):
    #    return

    #def Ver1_Ver3(self, cursor):
    #    return
