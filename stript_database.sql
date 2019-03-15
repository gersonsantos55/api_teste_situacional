CREATE DATABASE IF NOT EXISTS `teste_situacional`;
USE `teste_situacional`;

SET character_set_client = utf8;

DROP TABLE IF EXISTS `transferencia`;
DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(128) NOT NULL,
  `cnpj` varchar(14) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnpj_UNIQUE` (`cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `transferencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `pagador_nome` varchar(128) NOT NULL,
  `pagador_banco` varchar(3) NOT NULL,
  `pagador_agencia` varchar(4) NOT NULL,
  `pagador_conta` varchar(6) NOT NULL,
  `beneficiario_nome` varchar(128) NOT NULL,
  `beneficiario_banco` varchar(3) NOT NULL,
  `beneficiario_agencia` varchar(4) NOT NULL,
  `beneficiario_conta` varchar(6) NOT NULL,
  `valor` double(15,2) NOT NULL,
  `tipo` varchar(4) NOT NULL,
  `status` varchar(12) NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `data` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`usuario_id`),
  KEY `fk_transferencia_usuario_idx` (`usuario_id`),
  CONSTRAINT `fk_transferencia_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;


INSERT INTO `usuario` VALUES (1,'João Corp.','76443532000165'),
(2,'Maria Corp.','18823965000140');

INSERT INTO `transferencia` VALUES (1,1,'Antonio','001','0001','000001','Manuel','001','0001','000002',100.65,'CC','OK',1,'2019-03-13 01:00:00'),
(2,1,'Tony','001','0001','000003','Domingo','002','0001','000001',15.69,'DOC','OK',1,'2019-03-13 17:00:00'),
(3,1,'Manuel','001','0001','000002','Antonio','001','0001','000001',10.00,'CC','OK',1,'2019-03-13 12:00:00'),
(4,2,'Allan','002','0001','000002','Antonio','001','0001','000001',35.00,'TED','OK',1,'2019-03-13 12:00:00'),
(5,2,'Amanda','002','0001','000003','Tony','001','0001','000003',25.00,'DOC','OK',1,'2019-03-13 19:00:00'),
(6,2,'Domingo','002','0001','000001','Allan','002','0001','000002',16.00,'CC','OK',1,'2019-03-14 12:00:00'),
(7,2,'Manuel','001','0001','000002','Amanda','002','0001','000003',72.00,'DOC','OK',1,'2019-03-14 20:00:00'),
(8,1,'Allan','002','0001','000002','Manuel','001','0001','000002',46.00,'TED','OK',1,'2019-03-14 11:00:00'),
(9,1,'Amanda','002','0001','000003','Allan','002','0001','000002',58.00,'CC','OK',1,'2019-03-14 12:00:00'),
(10,1,'Allan','002','0001','000002','Domingo','002','0001','000001',96.00,'CC','OK',1,'2019-03-14 12:00:00');
