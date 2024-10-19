-- a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects - if no projects.name found in the table, you should create it
-- score, the score value for the correction

DELIMITER $$

CREATE PROCEDURE AddBonus(
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
)

BEGIN
	-- To check the project existence in project table
	DECLARE project_exist VARCHAR(255);	
	DECLARE target_project_id INT;

	SET project_exist = NULL;
        SET target_project_id  = 0;

	-- Query to retrive the project with name project name 
	SELECT name INTO project_exist FROM projects WHERE name = project_name;

	-- checking if project exist and if not we are inserting it to project table
	IF project_exist IS NULL THEN 
		INSERT INTO projects (name) VALUES (project_name);
	END IF;

	-- retrieving project id with name project_name
	SELECT id INTO target_project_id FROM projects WHERE name = project_name;

	-- Performing last insertion into corrections table
	INSERT INTO corrections(user_id, project_id, score)
	VALUES (user_id, target_project_id, score);


END $$

DELIMITER ;
