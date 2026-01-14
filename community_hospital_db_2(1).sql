/*
 Navicat Premium Dump SQL

 Source Server         : project
 Source Server Type    : MySQL
 Source Server Version : 80043 (8.0.43)
 Source Host           : localhost:3306
 Source Schema         : community_hospital_db_2

 Target Server Type    : MySQL
 Target Server Version : 80043 (8.0.43)
 File Encoding         : 65001

 Date: 21/12/2025 16:59:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for appointment
-- ----------------------------
DROP TABLE IF EXISTS `appointment`;
CREATE TABLE `appointment`  (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `schedule_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `expected_arrival` time NOT NULL,
  `status` enum('Scheduled','Confirmed','CheckedIn','Cancelled','Completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Scheduled',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`appointment_id`) USING BTREE,
  INDEX `schedule_id`(`schedule_id` ASC) USING BTREE,
  INDEX `idx_appointment_status`(`status` ASC) USING BTREE,
  INDEX `idx_appointment_date`(`appointment_date` ASC) USING BTREE,
  INDEX `idx_appointment_patient`(`patient_id` ASC, `status` ASC) USING BTREE,
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`schedule_id`) REFERENCES `schedule` (`schedule_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of appointment
-- ----------------------------
INSERT INTO `appointment` VALUES (1, 1, 1, '2025-12-21', '09:30:00', 'Completed', '2025-12-20 01:36:52', '网上预约，感冒症状');
INSERT INTO `appointment` VALUES (2, 2, 2, '2025-12-20', '15:00:00', 'Completed', '2025-12-20 01:36:52', '网上预约，儿童发热');

-- ----------------------------
-- Table structure for charge
-- ----------------------------
DROP TABLE IF EXISTS `charge`;
CREATE TABLE `charge`  (
  `charge_id` int NOT NULL AUTO_INCREMENT,
  `visit_id` int NOT NULL,
  `consultation_fee` decimal(10, 2) NULL DEFAULT 0.00,
  `medicine_fee` decimal(10, 2) NULL DEFAULT 0.00,
  `test_fee` decimal(10, 2) NULL DEFAULT 0.00,
  `other_fee` decimal(10, 2) NULL DEFAULT 0.00,
  `total_amount` decimal(10, 2) NOT NULL,
  `insurance_covered` decimal(10, 2) NULL DEFAULT 0.00,
  `self_pay` decimal(10, 2) NOT NULL,
  `payment_status` enum('Unpaid','PartiallyPaid','Paid','InsurancePending') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Unpaid',
  `payment_method` enum('Cash','Card','Insurance','WeChat','Alipay') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Cash',
  `payment_time` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`charge_id`) USING BTREE,
  UNIQUE INDEX `visit_id`(`visit_id` ASC) USING BTREE,
  INDEX `idx_charge_payment`(`payment_status` ASC, `payment_time` ASC) USING BTREE,
  CONSTRAINT `charge_ibfk_1` FOREIGN KEY (`visit_id`) REFERENCES `visit` (`visit_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of charge
-- ----------------------------
INSERT INTO `charge` VALUES (1, 1, 80.00, 120.50, 45.00, 10.00, 255.50, 180.00, 75.50, 'Paid', 'Insurance', '2025-12-20 01:38:27', '2025-12-20 01:38:27');
INSERT INTO `charge` VALUES (2, 2, 60.00, 85.00, 30.00, 5.00, 180.00, 100.00, 80.00, 'Paid', 'WeChat', '2025-12-20 01:38:27', '2025-12-20 01:38:27');

-- ----------------------------
-- Table structure for consultationroom
-- ----------------------------
DROP TABLE IF EXISTS `consultationroom`;
CREATE TABLE `consultationroom`  (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dept_id` int NULL DEFAULT NULL,
  `floor` int NULL DEFAULT NULL,
  `capacity` int NULL DEFAULT 1,
  `status` enum('Available','Occupied','Maintenance') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Available',
  PRIMARY KEY (`room_id`) USING BTREE,
  UNIQUE INDEX `room_number`(`room_number` ASC) USING BTREE,
  INDEX `dept_id`(`dept_id` ASC) USING BTREE,
  CONSTRAINT `consultationroom_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of consultationroom
-- ----------------------------
INSERT INTO `consultationroom` VALUES (1, '101', 1, 1, 1, 'Available');
INSERT INTO `consultationroom` VALUES (2, '102', 1, 1, 1, 'Available');
INSERT INTO `consultationroom` VALUES (3, '201', 2, 2, 2, 'Available');
INSERT INTO `consultationroom` VALUES (4, '202', 2, 2, 1, 'Available');
INSERT INTO `consultationroom` VALUES (5, '301', 3, 3, 1, 'Available');
INSERT INTO `consultationroom` VALUES (6, '302', 3, 3, 1, 'Maintenance');
INSERT INTO `consultationroom` VALUES (7, '401', 4, 4, 1, 'Available');
INSERT INTO `consultationroom` VALUES (8, '501', 5, 5, 2, 'Available');

-- ----------------------------
-- Table structure for dailyrevenue
-- ----------------------------
DROP TABLE IF EXISTS `dailyrevenue`;
CREATE TABLE `dailyrevenue`  (
  `revenue_date` date NOT NULL,
  `total_visits` int NULL DEFAULT 0,
  `total_revenue` decimal(15, 2) NULL DEFAULT 0.00,
  `insurance_revenue` decimal(15, 2) NULL DEFAULT 0.00,
  `cash_revenue` decimal(15, 2) NULL DEFAULT 0.00,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`revenue_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dailyrevenue
-- ----------------------------
INSERT INTO `dailyrevenue` VALUES ('2025-12-20', 2, 435.50, 280.00, 155.50, '2025-12-20 01:38:27');

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department`  (
  `dept_id` int NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dept_head` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES (1, '全科医学', '王明医生', '010-12345678', '成人普通医疗服务，常见病诊疗');
INSERT INTO `department` VALUES (2, '儿科', '李红医生', '010-12345679', '儿童和青少年医疗服务');
INSERT INTO `department` VALUES (3, '皮肤科', '张伟医生', '010-12345680', '皮肤病诊断与治疗，皮肤美容');
INSERT INTO `department` VALUES (4, '骨科', '刘峰医生', '010-12345681', '骨关节疾病诊疗，运动损伤康复');
INSERT INTO `department` VALUES (5, '急诊科', '陈夏医生', '010-12345682', '24小时急诊服务');

-- ----------------------------
-- Table structure for doctor
-- ----------------------------
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE `doctor`  (
  `doctor_id` int NOT NULL,
  `license_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `specialization` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `consultation_fee` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`doctor_id`) USING BTREE,
  UNIQUE INDEX `license_number`(`license_number` ASC) USING BTREE,
  CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `staff` (`staff_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of doctor
-- ----------------------------
INSERT INTO `doctor` VALUES (1, 'MED2020001', '内科、心血管疾病', 80.00);
INSERT INTO `doctor` VALUES (2, 'MED2020002', '儿科、儿童发育', 60.00);
INSERT INTO `doctor` VALUES (3, 'MED2020003', '皮肤科、皮肤美容', 100.00);
INSERT INTO `doctor` VALUES (4, 'MED2020004', '骨科、运动医学', 120.00);
INSERT INTO `doctor` VALUES (5, 'MED2022001', '急诊医学', 50.00);

-- ----------------------------
-- Table structure for patient
-- ----------------------------
DROP TABLE IF EXISTS `patient`;
CREATE TABLE `patient`  (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `id_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` enum('Male','Female','Other') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date_of_birth` date NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `emergency_contact` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `emergency_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `has_insurance` tinyint(1) NULL DEFAULT 0,
  `insurance_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `registration_date` date NOT NULL DEFAULT (curdate()),
  PRIMARY KEY (`patient_id`) USING BTREE,
  UNIQUE INDEX `id_number`(`id_number` ASC) USING BTREE,
  INDEX `idx_patient_name`(`full_name` ASC) USING BTREE,
  INDEX `idx_patient_phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patient
-- ----------------------------
INSERT INTO `patient` VALUES (1, '110101199001011234', '张三', 'Male', '1990-01-01', '13900139001', '北京市东城区', '李四', '13900139002', 1, 'INS20230001', '2025-12-20');
INSERT INTO `patient` VALUES (2, '110101199102022345', '李四', 'Female', '1991-02-02', '13900139003', '北京市海淀区', '张三', '13900139001', 1, 'INS20230002', '2025-12-20');
INSERT INTO `patient` VALUES (3, '110101198503033456', '王五', 'Male', '1985-03-03', '13900139004', '北京市朝阳区', '赵六', '13900139005', 0, NULL, '2025-12-20');
INSERT INTO `patient` VALUES (4, '110101201004044567', '赵六', 'Female', '2010-04-04', '13900139006', '北京市丰台区', '王五', '13900139004', 1, 'INS20230003', '2025-12-20');
INSERT INTO `patient` VALUES (5, '110101197605055678', '陈七', 'Male', '1976-05-05', '13900139007', '北京市石景山区', '陈八', '13900139008', 1, 'INS20230004', '2025-12-20');
INSERT INTO `patient` VALUES (6, '110101200108066789', '孙八', 'Female', '2001-08-06', '13900139009', '北京市西城区', '孙九', '13900139010', 1, 'INS20230005', '2025-12-20');

-- ----------------------------
-- Table structure for schedule
-- ----------------------------
DROP TABLE IF EXISTS `schedule`;
CREATE TABLE `schedule`  (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `room_id` int NOT NULL,
  `schedule_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `max_appointments` int NULL DEFAULT 20,
  `current_appointments` int NULL DEFAULT 0,
  `status` enum('Scheduled','InProgress','Completed','Cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Scheduled',
  PRIMARY KEY (`schedule_id`) USING BTREE,
  UNIQUE INDEX `unique_schedule`(`doctor_id` ASC, `schedule_date` ASC, `start_time` ASC) USING BTREE,
  INDEX `room_id`(`room_id` ASC) USING BTREE,
  INDEX `idx_schedule_date`(`schedule_date` ASC, `status` ASC) USING BTREE,
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `schedule_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `consultationroom` (`room_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of schedule
-- ----------------------------
INSERT INTO `schedule` VALUES (1, 1, 1, '2025-12-21', '09:00:00', '12:00:00', 10, 0, 'Completed');
INSERT INTO `schedule` VALUES (2, 2, 3, '2025-12-20', '14:00:00', '17:00:00', 8, 0, 'Completed');

-- ----------------------------
-- Table structure for staff
-- ----------------------------
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff`  (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `staff_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `staff_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` enum('Male','Female') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `position` enum('Doctor','Nurse','Administrative') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dept_id` int NULL DEFAULT NULL,
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `hire_date` date NOT NULL,
  `status` enum('Active','Inactive','OnLeave') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Active',
  PRIMARY KEY (`staff_id`) USING BTREE,
  UNIQUE INDEX `staff_number`(`staff_number` ASC) USING BTREE,
  INDEX `dept_id`(`dept_id` ASC) USING BTREE,
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of staff
-- ----------------------------
INSERT INTO `staff` VALUES (1, 'DOC001', '王明', 'Male', 'Doctor', 1, '主任医师', '13800138001', 'wangming@hospital.com', '2020-01-15', 'Active');
INSERT INTO `staff` VALUES (2, 'DOC002', '李红', 'Female', 'Doctor', 2, '主治医师', '13800138002', 'lihong@hospital.com', '2021-03-20', 'Active');
INSERT INTO `staff` VALUES (3, 'DOC003', '张伟', 'Male', 'Doctor', 3, '副主任医师', '13800138003', 'zhangwei@hospital.com', '2019-08-10', 'Active');
INSERT INTO `staff` VALUES (4, 'DOC004', '刘峰', 'Male', 'Doctor', 4, '主任医师', '13800138004', 'liufeng@hospital.com', '2018-05-12', 'Active');
INSERT INTO `staff` VALUES (5, 'DOC005', '陈夏', 'Female', 'Doctor', 5, '住院医师', '13800138005', 'chenxia@hospital.com', '2022-07-01', 'Active');
INSERT INTO `staff` VALUES (6, 'NUR001', '张丽', 'Female', 'Nurse', 1, '护士长', '13800138006', 'zhangli@hospital.com', '2019-02-14', 'Active');
INSERT INTO `staff` VALUES (7, 'NUR002', '王芳', 'Female', 'Nurse', 2, '资深护士', '13800138007', 'wangfang@hospital.com', '2020-09-22', 'Active');
INSERT INTO `staff` VALUES (8, 'NUR003', '李娜', 'Female', 'Nurse', 5, '急诊护士', '13800138010', 'lina_nurse@hospital.com', '2021-08-15', 'Active');
INSERT INTO `staff` VALUES (9, 'ADM001', '赵刚', 'Male', 'Administrative', NULL, '行政经理', '13800138008', 'zhaogang@hospital.com', '2017-11-05', 'Active');
INSERT INTO `staff` VALUES (10, 'ADM002', '刘静', 'Female', 'Administrative', NULL, '挂号收费员', '13800138009', 'liujing@hospital.com', '2021-04-18', 'Active');

-- ----------------------------
-- Table structure for visit
-- ----------------------------
DROP TABLE IF EXISTS `visit`;
CREATE TABLE `visit`  (
  `visit_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `room_id` int NOT NULL,
  `appointment_id` int NULL DEFAULT NULL,
  `checkin_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `checkout_time` timestamp NULL DEFAULT NULL,
  `symptoms` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `diagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `prescription` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `visit_status` enum('InProgress','Completed','Cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'InProgress',
  `created_by` int NULL DEFAULT NULL,
  PRIMARY KEY (`visit_id`) USING BTREE,
  INDEX `patient_id`(`patient_id` ASC) USING BTREE,
  INDEX `doctor_id`(`doctor_id` ASC) USING BTREE,
  INDEX `room_id`(`room_id` ASC) USING BTREE,
  INDEX `appointment_id`(`appointment_id` ASC) USING BTREE,
  INDEX `created_by`(`created_by` ASC) USING BTREE,
  INDEX `idx_visit_date`(`checkin_time` ASC) USING BTREE,
  CONSTRAINT `visit_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `visit_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `visit_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `consultationroom` (`room_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `visit_ibfk_4` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `visit_ibfk_5` FOREIGN KEY (`created_by`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of visit
-- ----------------------------
INSERT INTO `visit` VALUES (1, 1, 1, 1, 1, '2025-12-20 01:37:01', '2025-12-20 01:38:27', '咳嗽、流鼻涕、喉咙痛', '普通感冒', '感冒药*3天，多喝水，注意休息', 'Completed', 10);
INSERT INTO `visit` VALUES (2, 2, 2, 3, 2, '2025-12-20 01:37:01', '2025-12-20 01:38:27', '发热38.5℃，咳嗽', '上呼吸道感染', '退烧药，抗生素*5天，多休息', 'Completed', 10);

-- ----------------------------
-- View structure for availableschedules
-- ----------------------------
DROP VIEW IF EXISTS `availableschedules`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `availableschedules` AS select `s`.`schedule_id` AS `schedule_id`,`s`.`schedule_date` AS `schedule_date`,`s`.`start_time` AS `start_time`,`s`.`end_time` AS `end_time`,`s`.`max_appointments` AS `max_appointments`,`s`.`current_appointments` AS `current_appointments`,(`s`.`max_appointments` - `s`.`current_appointments`) AS `available_slots`,`st`.`staff_name` AS `doctor_name`,`st`.`title` AS `doctor_title`,`d`.`dept_name` AS `dept_name`,`cr`.`room_number` AS `room_number`,`doc`.`consultation_fee` AS `consultation_fee` from ((((`schedule` `s` join `doctor` `doc` on((`s`.`doctor_id` = `doc`.`doctor_id`))) join `staff` `st` on((`doc`.`doctor_id` = `st`.`staff_id`))) left join `department` `d` on((`st`.`dept_id` = `d`.`dept_id`))) join `consultationroom` `cr` on((`s`.`room_id` = `cr`.`room_id`))) where ((`s`.`schedule_date` >= curdate()) and (`s`.`status` = 'Scheduled') and (`s`.`current_appointments` < `s`.`max_appointments`) and (`cr`.`status` = 'Available'));

-- ----------------------------
-- View structure for currentpatients
-- ----------------------------
DROP VIEW IF EXISTS `currentpatients`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `currentpatients` AS select `v`.`visit_id` AS `visit_id`,`p`.`full_name` AS `patient_name`,`p`.`phone` AS `patient_phone`,`st`.`staff_name` AS `doctor_name`,`d`.`dept_name` AS `department`,`cr`.`room_number` AS `room_number`,`v`.`checkin_time` AS `checkin_time`,timediff(now(),`v`.`checkin_time`) AS `waiting_time` from (((((`visit` `v` join `patient` `p` on((`v`.`patient_id` = `p`.`patient_id`))) join `doctor` `doc` on((`v`.`doctor_id` = `doc`.`doctor_id`))) join `staff` `st` on((`doc`.`doctor_id` = `st`.`staff_id`))) left join `department` `d` on((`st`.`dept_id` = `d`.`dept_id`))) join `consultationroom` `cr` on((`v`.`room_id` = `cr`.`room_id`))) where (`v`.`visit_status` = 'InProgress');

-- ----------------------------
-- View structure for dailybillingsummary
-- ----------------------------
DROP VIEW IF EXISTS `dailybillingsummary`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `dailybillingsummary` AS select cast(`v`.`checkin_time` as date) AS `billing_date`,`d`.`dept_name` AS `dept_name`,`s`.`staff_name` AS `doctor_name`,count(distinct `v`.`visit_id`) AS `total_visits`,sum(`c`.`total_amount`) AS `total_revenue`,sum(`c`.`insurance_covered`) AS `insurance_revenue`,sum(`c`.`self_pay`) AS `self_pay_revenue`,group_concat(distinct `c`.`payment_method` separator ',') AS `payment_methods` from ((((`visit` `v` join `doctor` `doc` on((`v`.`doctor_id` = `doc`.`doctor_id`))) join `staff` `s` on((`doc`.`doctor_id` = `s`.`staff_id`))) join `department` `d` on((`s`.`dept_id` = `d`.`dept_id`))) join `charge` `c` on((`v`.`visit_id` = `c`.`visit_id`))) where (`c`.`payment_status` = 'Paid') group by cast(`v`.`checkin_time` as date),`d`.`dept_name`,`s`.`staff_name`;

-- ----------------------------
-- Procedure structure for CompleteVisitAndPayment
-- ----------------------------
DROP PROCEDURE IF EXISTS `CompleteVisitAndPayment`;
delimiter ;;
CREATE PROCEDURE `CompleteVisitAndPayment`(IN p_visit_id INT,
    IN p_symptoms TEXT,
    IN p_diagnosis TEXT,
    IN p_prescription TEXT,
    IN p_consultation_fee DECIMAL(10, 2),
    IN p_medicine_fee DECIMAL(10, 2),
    IN p_test_fee DECIMAL(10, 2),
    IN p_other_fee DECIMAL(10, 2),
    IN p_insurance_covered DECIMAL(10, 2),
    IN p_payment_method ENUM('Cash', 'Card', 'Insurance', 'WeChat', 'Alipay'),
    IN p_paid_by INT)
BEGIN
    DECLARE v_total_amount DECIMAL(10, 2);
    DECLARE v_self_pay DECIMAL(10, 2);
    DECLARE v_visit_date DATE;
    DECLARE v_room_id INT;
    DECLARE v_schedule_id INT;
    DECLARE v_appointment_id INT;
    
    -- 计算总金额和自付金额
    SET v_total_amount = p_consultation_fee + p_medicine_fee + p_test_fee + p_other_fee;
    SET v_self_pay = v_total_amount - p_insurance_covered;
    
    -- 获取就诊信息
    SELECT DATE(checkin_time), room_id, appointment_id INTO v_visit_date, v_room_id, v_appointment_id
    FROM Visit WHERE visit_id = p_visit_id;
    
    -- 如果有预约，获取排班ID
    IF v_appointment_id IS NOT NULL THEN
        SELECT schedule_id INTO v_schedule_id
        FROM Appointment WHERE appointment_id = v_appointment_id;
    END IF;
    
    -- 更新就诊记录
    UPDATE Visit 
    SET checkout_time = CURRENT_TIMESTAMP,
        visit_status = 'Completed',
        symptoms = p_symptoms,
        diagnosis = p_diagnosis,
        prescription = p_prescription
    WHERE visit_id = p_visit_id;
    
    -- 插入费用记录
    INSERT INTO Charge (
        visit_id,
        consultation_fee,
        medicine_fee,
        test_fee,
        other_fee,
        total_amount,
        insurance_covered,
        self_pay,
        payment_status,
        payment_method,
        payment_time
    ) VALUES (
        p_visit_id,
        p_consultation_fee,
        p_medicine_fee,
        p_test_fee,
        p_other_fee,
        v_total_amount,
        p_insurance_covered,
        v_self_pay,
        'Paid',
        p_payment_method,
        CURRENT_TIMESTAMP
    );
    
    -- 更新诊室状态
    UPDATE ConsultationRoom
    SET status = 'Available'
    WHERE room_id = v_room_id;
    
    -- 如果有预约，更新预约状态
    IF v_appointment_id IS NOT NULL THEN
        UPDATE Appointment 
        SET status = 'Completed'
        WHERE appointment_id = v_appointment_id;
    END IF;
    
    -- 如果有排班，更新排班状态并减少当前预约数
    IF v_schedule_id IS NOT NULL THEN
        UPDATE Schedule
        SET current_appointments = current_appointments - 1,
            status = CASE 
                WHEN current_appointments - 1 <= 0 THEN 'Completed'
                ELSE 'InProgress'
            END
        WHERE schedule_id = v_schedule_id;
    END IF;
    
    -- 更新每日收入统计
    INSERT INTO DailyRevenue (
        revenue_date,
        total_visits,
        total_revenue,
        insurance_revenue,
        cash_revenue
    ) VALUES (
        v_visit_date,
        1,
        v_total_amount,
        p_insurance_covered,
        v_self_pay
    ) ON DUPLICATE KEY UPDATE
        total_visits = total_visits + 1,
        total_revenue = total_revenue + v_total_amount,
        insurance_revenue = insurance_revenue + p_insurance_covered,
        cash_revenue = cash_revenue + v_self_pay;
    
    SELECT 'Visit completed and payment processed successfully' as message, 
           v_total_amount as total_amount, 
           v_self_pay as amount_paid,
           LAST_INSERT_ID() as charge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for CreateAppointment
-- ----------------------------
DROP PROCEDURE IF EXISTS `CreateAppointment`;
delimiter ;;
CREATE PROCEDURE `CreateAppointment`(IN p_patient_id INT,
    IN p_schedule_id INT,
    IN p_expected_arrival TIME,
    IN p_notes TEXT)
BEGIN
    DECLARE v_max_appointments INT;
    DECLARE v_current_appointments INT;
    DECLARE v_schedule_date DATE;
    
    -- 获取排班信息
    SELECT max_appointments, current_appointments, schedule_date
    INTO v_max_appointments, v_current_appointments, v_schedule_date
    FROM Schedule 
    WHERE schedule_id = p_schedule_id;
    
    -- 检查是否还有空位
    IF v_current_appointments >= v_max_appointments THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No available appointments for this schedule';
    END IF;
    
    -- 插入预约记录
    INSERT INTO Appointment (
        patient_id, 
        schedule_id, 
        appointment_date, 
        expected_arrival,
        notes
    ) VALUES (
        p_patient_id,
        p_schedule_id,
        v_schedule_date,
        p_expected_arrival,
        p_notes
    );
    
    -- 更新当前预约数
    UPDATE Schedule 
    SET current_appointments = current_appointments + 1
    WHERE schedule_id = p_schedule_id;
    
    SELECT LAST_INSERT_ID() as appointment_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for CreateSchedule
-- ----------------------------
DROP PROCEDURE IF EXISTS `CreateSchedule`;
delimiter ;;
CREATE PROCEDURE `CreateSchedule`(IN p_doctor_id INT,
    IN p_room_id INT,
    IN p_schedule_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_max_appointments INT)
BEGIN
    -- 检查医生是否在同一时间已有排班
    IF EXISTS (
        SELECT 1 FROM Schedule 
        WHERE doctor_id = p_doctor_id 
        AND schedule_date = p_schedule_date
        AND (
            (p_start_time BETWEEN start_time AND end_time) OR
            (p_end_time BETWEEN start_time AND end_time) OR
            (start_time BETWEEN p_start_time AND p_end_time)
        )
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Doctor already has a schedule at this time';
    END IF;
    
    -- 检查诊室是否在同一时间已被占用
    IF EXISTS (
        SELECT 1 FROM Schedule 
        WHERE room_id = p_room_id 
        AND schedule_date = p_schedule_date
        AND (
            (p_start_time BETWEEN start_time AND end_time) OR
            (p_end_time BETWEEN start_time AND end_time) OR
            (start_time BETWEEN p_start_time AND p_end_time)
        )
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Room is already occupied at this time';
    END IF;
    
    -- 插入排班记录
    INSERT INTO Schedule (
        doctor_id,
        room_id,
        schedule_date,
        start_time,
        end_time,
        max_appointments
    ) VALUES (
        p_doctor_id,
        p_room_id,
        p_schedule_date,
        p_start_time,
        p_end_time,
        p_max_appointments
    );
    
    SELECT 'Schedule created successfully' as message, LAST_INSERT_ID() as schedule_id;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for GetMonthlyRevenue
-- ----------------------------
DROP FUNCTION IF EXISTS `GetMonthlyRevenue`;
delimiter ;;
CREATE FUNCTION `GetMonthlyRevenue`(p_year INT, p_month INT)
 RETURNS decimal(15,2)
  READS SQL DATA 
  DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(15, 2);
    
    SELECT SUM(total_amount) INTO v_total
    FROM Charge c
    JOIN Visit v ON c.visit_id = v.visit_id
    WHERE YEAR(v.checkin_time) = p_year
    AND MONTH(v.checkin_time) = p_month
    AND c.payment_status = 'Paid';
    
    RETURN IFNULL(v_total, 0);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for PatientCheckIn
-- ----------------------------
DROP PROCEDURE IF EXISTS `PatientCheckIn`;
delimiter ;;
CREATE PROCEDURE `PatientCheckIn`(IN p_appointment_id INT,
    IN p_created_by INT)
BEGIN
    DECLARE v_patient_id INT;
    DECLARE v_doctor_id INT;
    DECLARE v_room_id INT;
    DECLARE v_schedule_id INT;
    DECLARE v_appointment_status VARCHAR(20);
    
    -- 获取预约信息和状态
    SELECT a.patient_id, s.doctor_id, s.room_id, a.schedule_id, a.status
    INTO v_patient_id, v_doctor_id, v_room_id, v_schedule_id, v_appointment_status
    FROM Appointment a
    JOIN Schedule s ON a.schedule_id = s.schedule_id
    WHERE a.appointment_id = p_appointment_id;
    
    IF v_patient_id IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Appointment not found';
    END IF;
    
    IF v_appointment_status = 'Cancelled' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Cannot check in a cancelled appointment';
    END IF;
    
    -- 创建就诊记录
    INSERT INTO Visit (
        patient_id,
        doctor_id,
        room_id,
        appointment_id,
        created_by
    ) VALUES (
        v_patient_id,
        v_doctor_id,
        v_room_id,
        p_appointment_id,
        p_created_by
    );
    
    -- 更新预约状态
    UPDATE Appointment 
    SET status = 'CheckedIn'
    WHERE appointment_id = p_appointment_id;
    
    -- 更新诊室状态
    UPDATE ConsultationRoom
    SET status = 'Occupied'
    WHERE room_id = v_room_id;
    
    -- 更新排班状态
    UPDATE Schedule
    SET status = 'InProgress'
    WHERE schedule_id = v_schedule_id;
    
    SELECT 'Patient checked in successfully' as message, LAST_INSERT_ID() as visit_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for ProcessPayment
-- ----------------------------
DROP PROCEDURE IF EXISTS `ProcessPayment`;
delimiter ;;
CREATE PROCEDURE `ProcessPayment`(IN p_visit_id INT,
    IN p_consultation_fee DECIMAL(10, 2),
    IN p_medicine_fee DECIMAL(10, 2),
    IN p_test_fee DECIMAL(10, 2),
    IN p_other_fee DECIMAL(10, 2),
    IN p_insurance_covered DECIMAL(10, 2),
    IN p_payment_method ENUM('Cash', 'Card', 'Insurance', 'WeChat', 'Alipay'))
BEGIN
    DECLARE v_total_amount DECIMAL(10, 2);
    DECLARE v_self_pay DECIMAL(10, 2);
    DECLARE v_visit_date DATE;
    
    -- 计算总金额和自付金额
    SET v_total_amount = p_consultation_fee + p_medicine_fee + p_test_fee + p_other_fee;
    SET v_self_pay = v_total_amount - p_insurance_covered;
    
    -- 获取就诊日期
    SELECT DATE(checkin_time) INTO v_visit_date
    FROM Visit WHERE visit_id = p_visit_id;
    
    -- 插入费用记录
    INSERT INTO Charge (
        visit_id,
        consultation_fee,
        medicine_fee,
        test_fee,
        other_fee,
        total_amount,
        insurance_covered,
        self_pay,
        payment_status,
        payment_method,
        payment_time
    ) VALUES (
        p_visit_id,
        p_consultation_fee,
        p_medicine_fee,
        p_test_fee,
        p_other_fee,
        v_total_amount,
        p_insurance_covered,
        v_self_pay,
        'Paid',
        p_payment_method,
        CURRENT_TIMESTAMP
    );
    
    -- 更新就诊状态
    UPDATE Visit 
    SET checkout_time = CURRENT_TIMESTAMP,
        visit_status = 'Completed'
    WHERE visit_id = p_visit_id;
    
    -- 更新诊室状态
    UPDATE ConsultationRoom cr
    JOIN Visit v ON cr.room_id = v.room_id
    SET cr.status = 'Available'
    WHERE v.visit_id = p_visit_id;
    
    -- 更新每日收入统计
    INSERT INTO DailyRevenue (
        revenue_date,
        total_visits,
        total_revenue,
        insurance_revenue,
        cash_revenue
    ) VALUES (
        v_visit_date,
        1,
        v_total_amount,
        p_insurance_covered,
        v_self_pay
    ) ON DUPLICATE KEY UPDATE
        total_visits = total_visits + 1,
        total_revenue = total_revenue + v_total_amount,
        insurance_revenue = insurance_revenue + p_insurance_covered,
        cash_revenue = cash_revenue + v_self_pay;
    
    SELECT LAST_INSERT_ID() as charge_id;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table charge
-- ----------------------------
DROP TRIGGER IF EXISTS `ValidateChargeAmount`;
delimiter ;;
CREATE TRIGGER `ValidateChargeAmount` BEFORE INSERT ON `charge` FOR EACH ROW BEGIN
    DECLARE expected_total DECIMAL(10, 2);
    
    SET expected_total = NEW.consultation_fee + NEW.medicine_fee + 
                        NEW.test_fee + NEW.other_fee;
    
    IF NEW.total_amount != expected_total THEN
        SET NEW.total_amount = expected_total;
    END IF;
    
    IF NEW.self_pay != (NEW.total_amount - NEW.insurance_covered) THEN
        SET NEW.self_pay = NEW.total_amount - NEW.insurance_covered;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table schedule
-- ----------------------------
DROP TRIGGER IF EXISTS `UpdateDoctorStatus`;
delimiter ;;
CREATE TRIGGER `UpdateDoctorStatus` AFTER INSERT ON `schedule` FOR EACH ROW BEGIN
    -- 当医生有排班时，标记为Active
    UPDATE Staff 
    SET status = 'Active'
    WHERE staff_id = NEW.doctor_id
    AND status != 'OnLeave';
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
