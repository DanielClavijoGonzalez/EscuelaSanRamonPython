CREATE SCHEMA escuela;
USE escuela;

CREATE TABLE `cursos` (
  `id` int(11) NOT NULL,
  `profesor_encargado` int(11) NOT NULL,
  `grado` tinyint(2) NOT NULL
);

CREATE TABLE `estudiantes` (
  `id` int(11) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `curso` int(11) NOT NULL,
  `documento_identidad` int(20) NOT NULL
);

CREATE TABLE `materias` (
  `id` int(11) NOT NULL,
  `nombre_materia` varchar(20) NOT NULL,
  `profesor` int(11) NOT NULL
);

CREATE TABLE `notas` (
  `id` int(11) NOT NULL,
  `nota1` double NOT NULL,
  `nota2` double NOT NULL,
  `nota3` double NOT NULL,
  `nota4` double NOT NULL,
  `estudiante` int(11) NOT NULL,
  `materia` int(11) NOT NULL
);

CREATE TABLE `profesores` (
  `id` int(11) NOT NULL,
  `nombre` varchar(25) NOT NULL,
  `asignatura` varchar(20) NOT NULL
);

ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profesor_encargado` (`profesor_encargado`);

ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `curso` (`curso`);

ALTER TABLE `materias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profesor` (`profesor`);

ALTER TABLE `notas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estudiante` (`estudiante`),
  ADD KEY `materia` (`materia`);

ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `cursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;


ALTER TABLE `estudiantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `materias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `notas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `profesores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`profesor_encargado`) REFERENCES `profesores` (`id`);

ALTER TABLE `estudiantes`
  ADD CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`curso`) REFERENCES `cursos` (`id`);

ALTER TABLE `materias`
  ADD CONSTRAINT `materias_ibfk_1` FOREIGN KEY (`profesor`) REFERENCES `profesores` (`id`);

ALTER TABLE `notas`
  ADD CONSTRAINT `notas_ibfk_1` FOREIGN KEY (`estudiante`) REFERENCES `estudiantes` (`id`),
  ADD CONSTRAINT `notas_ibfk_2` FOREIGN KEY (`materia`) REFERENCES `materias` (`id`);
COMMIT;