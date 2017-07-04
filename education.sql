/*
MySQL Data Transfer
Source Host: localhost
Source Database: education
Target Host: localhost
Target Database: education
Date: 2017/5/22 23:35:46
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for course
-- ----------------------------
CREATE TABLE `course` (
  `courseID` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) DEFAULT NULL,
  `credit` int(11) DEFAULT NULL,
  PRIMARY KEY (`courseID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for take
-- ----------------------------
CREATE TABLE `take` (
  `grade` int(11) DEFAULT NULL,
  `userid` int(11) NOT NULL,
  `courseid` int(11) NOT NULL,
  PRIMARY KEY (`userid`,`courseid`),
  KEY `cid` (`courseid`),
  CONSTRAINT `cid` FOREIGN KEY (`courseid`) REFERENCES `course` (`courseID`),
  CONSTRAINT `uid` FOREIGN KEY (`userid`) REFERENCES `user` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
CREATE TABLE `teacher` (
  `teacheID` varchar(10) NOT NULL,
  `name` varchar(10) NOT NULL,
  `salary` int(11) DEFAULT NULL,
  PRIMARY KEY (`teacheID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
CREATE TABLE `user` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `tel` varchar(11) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `age` int(3) DEFAULT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records 
-- ----------------------------
INSERT INTO `course` VALUES ('1', '数据挖掘', '3');
INSERT INTO `course` VALUES ('2', '软件工程', '2');
INSERT INTO `course` VALUES ('3', '算法导论', '3');
INSERT INTO `take` VALUES (null, '1', '1');
INSERT INTO `take` VALUES (null, '1', '3');
INSERT INTO `user` VALUES ('1', null, 'ryc', '1234', '', 'm', '18826101010', null, null);
INSERT INTO `user` VALUES ('2', null, 'sai', '123', '', null, '18826101010', null, null);
INSERT INTO `user` VALUES ('8', null, '薛川', '123', '', null, '18826130628', null, null);
INSERT INTO `user` VALUES ('9', null, '阿萨德', '123', '442122291@qq.com', null, null, null, null);
INSERT INTO `user` VALUES ('10', null, '打打撒', '123456', '574002967@qq.com', null, null, null, null);
INSERT INTO `user` VALUES ('11', null, 'dsfa', '123123', '123', null, null, null, null);
INSERT INTO `user` VALUES ('12', null, 'sai1996', '123456', '469970581@qq.com', null, null, null, null);
