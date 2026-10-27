-- 由开发库 flask_data 导出（结构 + 初始数据）。
-- 警告：脚本包含 DROP TABLE，导入前请确认目标库数据可被覆盖。


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `flask_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `flask_data`;
DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `goods_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `goods_id` (`goods_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`goods_id`) REFERENCES `goods` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (50,59,7,1,'2025-12-01 16:50:57'),(51,59,10,1,'2025-12-01 16:51:00'),(52,59,6,1,'2025-12-01 16:51:02');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `detail` varchar(200) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `sales` int DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `goods` WRITE;
/*!40000 ALTER TABLE `goods` DISABLE KEYS */;
INSERT INTO `goods` VALUES (6,'北流凉亭鸡','凉亭鸡颈部羽毛金黄色、喙及脚胫黄色、羽毛紧凑、毛片较细、较薄、体型中等，体躯结实。凉亭鸡体躯微型，结实紧凑，啄、脚及皮肤均为淡黄色，皮薄骨细，皮下及肌间脂肪含量适中，分布均匀，肉质细嫩，肉味香浓，清甜爽口，风味独特。','30',163,'北流凉亭鸡.webp'),(7,'北流桂圆干','桂圆干又名益智、龙眼肉，为龙眼的成熟果实，性平，味甘，含有硫胺素、核黄素、尼克酸、抗坏血酸等化学成份，具有益气补血，安神定志，养血安胎的功效。 北流市具备有种植亚热带水果龙眼的良好气候条件，全市拥有龙眼种植面积16万多亩，年产石硖、大乌圆等优质龙眼3万多吨，年加工优质桂圆干5000多吨。 北流市早在1998年被广西壮族自治区人民政府评为“全区十强水果县（市）”。','9',206,'北流桂圆干.jpg'),(8,'北流荔枝','北流荔枝以桂味、鸡嘴荔、淮荔（禾荔）为代表：桂味：果圆球形或近圆球形，中等大；果皮浅红色，皮薄；果肩平，果顶浑圆；龟裂片凸起，裂片峰尖锐刺手，缝合线明显；果肉蜡白色，肉质爽脆，汁多，味清甜，有桂花香味，焦核。鸡嘴荔：果歪心形或扁圆形；果大。果皮暗红色，皮薄、韧；果肩一平一隆起，果顶浑圆。龟裂片平坦或乳状突起，裂片峰锐尖。缝合线有，不明显。果肉蜡白色，肉质爽脆，汁中等，味清甜，微香。核小似小鸡嘴','20',1028,'北流荔枝.webp'),(9,'北流陶瓷','北流陶瓷是广西北流市重要支柱产业和北流五宝之一，起源于夏商时期，唐代圭江两岸出现制陶活动，宋代岭垌窑达到兴盛阶段，其青白瓷工艺成熟并在广西陶瓷史上占据重要地位，产品远销海外 [3] [5-6]。元明时期产业衰落，清代康乾年间逐步恢复，至民国时期形成22家瓷厂，成为广西第二大瓷器生产基地','9.9',503,'北流陶瓷.webp'),(10,'北流鸭塘鱼','鸭塘鱼是广西北流市北流镇凉水井村鸭儿塘出产的软骨鱼，广西五种地方传统名菜之一，因塘形似鸭得名，主要品种有鲫、鲮、鲤、草鱼等。该塘有上百个常年不涸的泉眼，泉水富含硒等微量元素，对鱼骨产生特殊软化作用，形成骨刺脆软、肉质肥嫩的特征，烹饪后无腥味且煎制不粘锅 [3] [5-6]。鱼尾呈缺角状，体型较小，鲮鱼仅拇指大小，养殖时不投喂人工饲料','27.08',307,'北流鸭塘鱼.webp'),(11,'广西肉桂','广西肉桂，广西壮族自治区南部亚热带地区特产，中国地理标志产品。该地区独特的自然环境条件，悠久的栽培历史，传统的生产农艺和加工工艺，形成了广西肉桂皮厚、色泽光润、含油率高、味辛香偏辣、药用和调香料用兼优等特点。桂皮出口和桂油的加工出口量均占全国总量的60%以上。\n','86.51',31,'广西肉桂.webp'),(12,'炒米糖','炒米糖是广西传统特色小吃，以糯米为主料，经浸米、蒸米、碓臼、砂炒膨化等工序制成，通过挂霜工艺形成黄亮酥脆、甜而不腻的蜂蛹状糖品 [2-3]。其制作强调米粒完整与火候掌控，需用糖油粘合塑形后密封储存，常见于春节期间，兼具零食与节庆礼仪功能','15.5',50,'炒米糖.webp'),(13,'玉林大蒜头','玉林大蒜头是广西玉林地区的特色农产品，栽培历史逾千年，主产于仁东、仁厚、福绵等地。其表皮多呈紫色或白色，以粒瓣结实、辛辣多汁、肉脆味香著称，采用冬种夏收模式种植，经烟熏处理后可长期贮存。该品种富含蛋白质、维生素等成分，兼具调味与药用功能','2',200,'玉林大蒜头.webp'),(14,'玉林正骨水','玉林正骨水是广西玉林制药有限责任公司根据五十年代初期富有传奇经历的著名老中医陈善文先生献出的祖传秘方，结合现代技术研制而成的纯中药制剂，具有驳骨、镇痛、消肿和旺盛局部血液循环，促进新陈代谢等作用，对跌打损伤及消除运动疲劳功效卓著。','99',24,'玉林正骨水.webp');
/*!40000 ALTER TABLE `goods` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `tel` varchar(20) DEFAULT NULL,
  `img` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES (1,'徐嘉','202309602001','1.jpg'),(2,'陈善美','202309602002','2.jpg'),(3,'覃秀免','202309602003','3.png'),(4,'卢焕蓉','202309602004','4.jpg'),(5,'陆碧霞','202309602005','5.png'),(6,'陈海凤','202309602006','6.jpg'),(7,'黄敏怡','202309602007','7.jpg'),(8,'唐秋菊','202309602008','8.jpg'),(9,'谢雯煜','202309602009','9.jpg'),(10,'梁艳春','202309602010','10.jpg'),(11,'戴金蓉','202309602011','11.jpg'),(12,'巫玉安','202309602012','12.jpg'),(13,'朱丽艳','202309602013','13.jpg'),(14,'谢俏奕','202309602014','14.jpg'),(15,'杜康磊','202309602015','15.jpg'),(16,'冉子昊','202309602016','16.jpg'),(17,'韦林强','202309602017','17.jpg'),(18,'马明闯','202309602018','18.jpg'),(19,'邓顺德','202309602019','19.jpg'),(20,'王铭宇','202309602020','20.jpg'),(21,'束邦国','202309602021','21.jpg'),(22,'李城强','202309602022','22.jpg'),(23,'李甲桂','202309602023','23.jpg'),(24,'郭益新','202309602024','24.jpg'),(25,'石博轩','202309602025','25.jpg'),(26,'冯嘉伟','202309602026','26.jpg'),(27,'梁先锐','202309602027','27.jpg'),(28,'唐寄邕','202309602028','28.jpg'),(29,'姚开廷','202309602029','29.jpg'),(30,'陈语成','202309602030','30.jpg'),(31,'韦晔','202309602031','31.jpg'),(32,'翟可誉','202309602032','32.jpg'),(33,'庞凯友','202309602033','33.jpg'),(34,'江文庆','202309602034','34.jpg'),(35,'田洪桔','202309602035','35.jpg'),(36,'韦世昌','202309602036','36.jpg'),(37,'李伟杰','202309602037','37.jpg'),(38,'裴文博','202309602038','38.jpg'),(39,'宋承宪','202309602039','39.jpg'),(40,'何永飞','202309602040','40.jpg'),(41,'陈泽','202309602041','41.jpg'),(42,'张博涵','202309602042','42.jpg'),(43,'杨莹','202309602043','43.jpg'),(44,'韦贝贝','202309602044','44.jpg'),(45,'陈东玲','202309602045','45.jpg'),(46,'杨妮新','202309602046','46.jpg'),(47,'覃玉春','202309602047','47.jpg'),(48,'李思蓓','202309602048','48.jpg'),(49,'李苑霏','202309602049','49.jpg'),(50,'周美霞','202309602050','50.jpg'),(51,'马伟英','202309602051','51.jpg'),(52,'黄李婷','202309602052','52.jpg'),(53,'黄潇潇','202309602053','53.jpg');
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `telephone` varchar(64) DEFAULT NULL,
  `img` varchar(211) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (58,'hdtljg123','scrypt:32768:8:1$R4GjOVFzCVdChRMp$9d1493d165c606060863bfe4f3e237484a927407706fc6cb2f4bdbdff94088b0a19e4f558da43608ee18923cca3bd38298bbda8f7688b41a883309c80e12e8ed','16578945127','1764250107.20','user'),(59,'zhangsan','scrypt:32768:8:1$eTbU6GS4jJ7irXOP$a27e570fc31a5d93d77d4b202cc5e030496b35a8f95bc389e5db0273293d756c2a3b75a674bf37077c56a1576d522e1c197083213dea9063f807776ff08a51cb','16578945324',NULL,'admin'),(63,'hdtljg','scrypt:32768:8:1$mwZ8Tf18nXOJhKsl$b54e2b561027c2bc2c356326c7d635772e731de33cc0fa82ed59032a5866eb7a8c5f626dfddfa5cee1f94db782c25f0afdf674987cb5d46c28e93044584687ff','15678945611','1764250400.jpg','user'),(65,'hdtljg666','scrypt:32768:8:1$VJLUw0DaaBg4I9rl$83a6e32ee9cde4c707aa22991850782a21f80a6f66aed9779a58fbffa4aa45e6699179f18485318d166fe7ea79caa1824d60f40bab214393d2ed333cc0ca7081','19877571216','1793007341.jpg','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

