-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-11-2025 a las 04:31:41
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `inventario_lime`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_condicionesfuncionamiento`
--

CREATE TABLE `api_condicionesfuncionamiento` (
  `id` bigint(20) NOT NULL,
  `voltaje` varchar(50) NOT NULL,
  `corriente` varchar(50) DEFAULT NULL,
  `humedad` varchar(50) DEFAULT NULL,
  `temperatura` varchar(100) DEFAULT NULL,
  `dimensiones` varchar(200) NOT NULL,
  `peso` varchar(50) NOT NULL,
  `otros` varchar(200) DEFAULT NULL,
  `equipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_documentoequipo`
--

CREATE TABLE `api_documentoequipo` (
  `id` bigint(20) NOT NULL,
  `hoja_vida` tinyint(1) NOT NULL,
  `registro_importacion` tinyint(1) NOT NULL,
  `manual_operacion` tinyint(1) NOT NULL,
  `manual_mantenimiento` varchar(200) DEFAULT NULL,
  `guia_rapida` tinyint(1) NOT NULL,
  `instructivo_manejo` tinyint(1) NOT NULL,
  `protocolo_mantenimiento` tinyint(1) NOT NULL,
  `frecuencia_metrologica` varchar(100) DEFAULT NULL,
  `equipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_equipo`
--

CREATE TABLE `api_equipo` (
  `id` bigint(20) NOT NULL,
  `proceso` varchar(200) NOT NULL,
  `nombre_equipo` varchar(200) NOT NULL,
  `codigo_inventario` varchar(100) NOT NULL,
  `codigo_ips` varchar(100) DEFAULT NULL,
  `codigo_ecri` varchar(100) DEFAULT NULL,
  `ubicacion_fisica` varchar(200) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `modelo` varchar(100) NOT NULL,
  `serie` varchar(150) NOT NULL,
  `clasificacion_misional` varchar(200) DEFAULT NULL,
  `clasificacion_ips` varchar(100) DEFAULT NULL,
  `clasificacion_riesgo` varchar(100) DEFAULT NULL,
  `registro_invima` varchar(200) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `descripcion_baja` longtext DEFAULT NULL,
  `fecha_baja` date DEFAULT NULL,
  `responsable_id` bigint(20) DEFAULT NULL,
  `sede_id` bigint(20) DEFAULT NULL,
  `servicio_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_metrologiaadmin`
--

CREATE TABLE `api_metrologiaadmin` (
  `id` bigint(20) NOT NULL,
  `mantenimiento` tinyint(1) NOT NULL,
  `frecuencia_mantenimiento` int(11) NOT NULL,
  `calibracion` tinyint(1) NOT NULL,
  `frecuencia_calibracion` varchar(100) DEFAULT NULL,
  `equipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_metrologiatecnica`
--

CREATE TABLE `api_metrologiatecnica` (
  `id` bigint(20) NOT NULL,
  `magnitud` varchar(150) NOT NULL,
  `rango_equipo` varchar(200) NOT NULL,
  `resolucion` varchar(100) DEFAULT NULL,
  `rango_trabajo` varchar(200) NOT NULL,
  `error_maximo` varchar(100) DEFAULT NULL,
  `equipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_registrohistorico`
--

CREATE TABLE `api_registrohistorico` (
  `id` bigint(20) NOT NULL,
  `tiempo_vida_util` varchar(50) DEFAULT NULL,
  `fecha_adquisicion` date DEFAULT NULL,
  `propietario` varchar(100) NOT NULL,
  `fecha_fabricacion` varchar(50) DEFAULT NULL,
  `nit` varchar(50) NOT NULL,
  `proveedor` varchar(200) NOT NULL,
  `en_garantia` tinyint(1) NOT NULL,
  `fecha_fin_garantia` varchar(100) DEFAULT NULL,
  `forma_adquisicion` varchar(100) NOT NULL,
  `tipo_documento` varchar(50) NOT NULL,
  `numero_documento` varchar(100) NOT NULL,
  `equipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_responsable`
--

CREATE TABLE `api_responsable` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_sede`
--

CREATE TABLE `api_sede` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `api_servicio`
--

CREATE TABLE `api_servicio` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `sede_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add equipo', 7, 'add_equipo'),
(26, 'Can change equipo', 7, 'change_equipo'),
(27, 'Can delete equipo', 7, 'delete_equipo'),
(28, 'Can view equipo', 7, 'view_equipo'),
(29, 'Can add responsable', 8, 'add_responsable'),
(30, 'Can change responsable', 8, 'change_responsable'),
(31, 'Can delete responsable', 8, 'delete_responsable'),
(32, 'Can view responsable', 8, 'view_responsable'),
(33, 'Can add sede', 9, 'add_sede'),
(34, 'Can change sede', 9, 'change_sede'),
(35, 'Can delete sede', 9, 'delete_sede'),
(36, 'Can view sede', 9, 'view_sede'),
(37, 'Can add servicio', 10, 'add_servicio'),
(38, 'Can change servicio', 10, 'change_servicio'),
(39, 'Can delete servicio', 10, 'delete_servicio'),
(40, 'Can view servicio', 10, 'view_servicio'),
(41, 'Can add registro historico', 11, 'add_registrohistorico'),
(42, 'Can change registro historico', 11, 'change_registrohistorico'),
(43, 'Can delete registro historico', 11, 'delete_registrohistorico'),
(44, 'Can view registro historico', 11, 'view_registrohistorico'),
(45, 'Can add metrologia tecnica', 12, 'add_metrologiatecnica'),
(46, 'Can change metrologia tecnica', 12, 'change_metrologiatecnica'),
(47, 'Can delete metrologia tecnica', 12, 'delete_metrologiatecnica'),
(48, 'Can view metrologia tecnica', 12, 'view_metrologiatecnica'),
(49, 'Can add metrologia admin', 13, 'add_metrologiaadmin'),
(50, 'Can change metrologia admin', 13, 'change_metrologiaadmin'),
(51, 'Can delete metrologia admin', 13, 'delete_metrologiaadmin'),
(52, 'Can view metrologia admin', 13, 'view_metrologiaadmin'),
(53, 'Can add documento equipo', 14, 'add_documentoequipo'),
(54, 'Can change documento equipo', 14, 'change_documentoequipo'),
(55, 'Can delete documento equipo', 14, 'delete_documentoequipo'),
(56, 'Can view documento equipo', 14, 'view_documentoequipo'),
(57, 'Can add condiciones funcionamiento', 15, 'add_condicionesfuncionamiento'),
(58, 'Can change condiciones funcionamiento', 15, 'change_condicionesfuncionamiento'),
(59, 'Can delete condiciones funcionamiento', 15, 'delete_condicionesfuncionamiento'),
(60, 'Can view condiciones funcionamiento', 15, 'view_condicionesfuncionamiento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(15, 'api', 'condicionesfuncionamiento'),
(14, 'api', 'documentoequipo'),
(7, 'api', 'equipo'),
(13, 'api', 'metrologiaadmin'),
(12, 'api', 'metrologiatecnica'),
(11, 'api', 'registrohistorico'),
(8, 'api', 'responsable'),
(9, 'api', 'sede'),
(10, 'api', 'servicio'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-17 03:28:28.651736'),
(2, 'auth', '0001_initial', '2025-11-17 03:28:29.684969'),
(3, 'admin', '0001_initial', '2025-11-17 03:28:29.967307'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-17 03:28:29.981498'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-17 03:28:30.007322'),
(6, 'api', '0001_initial', '2025-11-17 03:28:31.550307'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-11-17 03:28:31.697992'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-11-17 03:28:31.799569'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-11-17 03:28:31.833586'),
(10, 'auth', '0004_alter_user_username_opts', '2025-11-17 03:28:31.848842'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-11-17 03:28:31.962269'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-11-17 03:28:31.968609'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-11-17 03:28:31.988765'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-11-17 03:28:32.022851'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-11-17 03:28:32.056754'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-11-17 03:28:32.086784'),
(17, 'auth', '0011_update_proxy_permissions', '2025-11-17 03:28:32.124537'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-11-17 03:28:32.159695'),
(19, 'sessions', '0001_initial', '2025-11-17 03:28:32.218643');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `api_condicionesfuncionamiento`
--
ALTER TABLE `api_condicionesfuncionamiento`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `equipo_id` (`equipo_id`);

--
-- Indices de la tabla `api_documentoequipo`
--
ALTER TABLE `api_documentoequipo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `equipo_id` (`equipo_id`);

--
-- Indices de la tabla `api_equipo`
--
ALTER TABLE `api_equipo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `api_equipo_responsable_id_8801648e_fk_api_responsable_id` (`responsable_id`),
  ADD KEY `api_equipo_sede_id_2405820b_fk_api_sede_id` (`sede_id`),
  ADD KEY `api_equipo_servicio_id_57d015af_fk_api_servicio_id` (`servicio_id`);

--
-- Indices de la tabla `api_metrologiaadmin`
--
ALTER TABLE `api_metrologiaadmin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `equipo_id` (`equipo_id`);

--
-- Indices de la tabla `api_metrologiatecnica`
--
ALTER TABLE `api_metrologiatecnica`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `equipo_id` (`equipo_id`);

--
-- Indices de la tabla `api_registrohistorico`
--
ALTER TABLE `api_registrohistorico`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `equipo_id` (`equipo_id`);

--
-- Indices de la tabla `api_responsable`
--
ALTER TABLE `api_responsable`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `api_sede`
--
ALTER TABLE `api_sede`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `api_servicio`
--
ALTER TABLE `api_servicio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `api_servicio_sede_id_f531977a_fk_api_sede_id` (`sede_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `api_condicionesfuncionamiento`
--
ALTER TABLE `api_condicionesfuncionamiento`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_documentoequipo`
--
ALTER TABLE `api_documentoequipo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_equipo`
--
ALTER TABLE `api_equipo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_metrologiaadmin`
--
ALTER TABLE `api_metrologiaadmin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_metrologiatecnica`
--
ALTER TABLE `api_metrologiatecnica`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_registrohistorico`
--
ALTER TABLE `api_registrohistorico`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_responsable`
--
ALTER TABLE `api_responsable`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_sede`
--
ALTER TABLE `api_sede`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `api_servicio`
--
ALTER TABLE `api_servicio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `api_condicionesfuncionamiento`
--
ALTER TABLE `api_condicionesfuncionamiento`
  ADD CONSTRAINT `api_condicionesfunci_equipo_id_ff3f27fc_fk_api_equip` FOREIGN KEY (`equipo_id`) REFERENCES `api_equipo` (`id`);

--
-- Filtros para la tabla `api_documentoequipo`
--
ALTER TABLE `api_documentoequipo`
  ADD CONSTRAINT `api_documentoequipo_equipo_id_d007bbd5_fk_api_equipo_id` FOREIGN KEY (`equipo_id`) REFERENCES `api_equipo` (`id`);

--
-- Filtros para la tabla `api_equipo`
--
ALTER TABLE `api_equipo`
  ADD CONSTRAINT `api_equipo_responsable_id_8801648e_fk_api_responsable_id` FOREIGN KEY (`responsable_id`) REFERENCES `api_responsable` (`id`),
  ADD CONSTRAINT `api_equipo_sede_id_2405820b_fk_api_sede_id` FOREIGN KEY (`sede_id`) REFERENCES `api_sede` (`id`),
  ADD CONSTRAINT `api_equipo_servicio_id_57d015af_fk_api_servicio_id` FOREIGN KEY (`servicio_id`) REFERENCES `api_servicio` (`id`);

--
-- Filtros para la tabla `api_metrologiaadmin`
--
ALTER TABLE `api_metrologiaadmin`
  ADD CONSTRAINT `api_metrologiaadmin_equipo_id_02afdd80_fk_api_equipo_id` FOREIGN KEY (`equipo_id`) REFERENCES `api_equipo` (`id`);

--
-- Filtros para la tabla `api_metrologiatecnica`
--
ALTER TABLE `api_metrologiatecnica`
  ADD CONSTRAINT `api_metrologiatecnica_equipo_id_75c0ab38_fk_api_equipo_id` FOREIGN KEY (`equipo_id`) REFERENCES `api_equipo` (`id`);

--
-- Filtros para la tabla `api_registrohistorico`
--
ALTER TABLE `api_registrohistorico`
  ADD CONSTRAINT `api_registrohistorico_equipo_id_d8ba176b_fk_api_equipo_id` FOREIGN KEY (`equipo_id`) REFERENCES `api_equipo` (`id`);

--
-- Filtros para la tabla `api_servicio`
--
ALTER TABLE `api_servicio`
  ADD CONSTRAINT `api_servicio_sede_id_f531977a_fk_api_sede_id` FOREIGN KEY (`sede_id`) REFERENCES `api_sede` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
