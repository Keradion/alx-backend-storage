-- a SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
	IN target_user_id INT
)
BEGIN
	-- comuputing the average score of user with target_user_id
        
	DECLARE avg_score DECIMAL;
	
	SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = target_user_id;
        
	-- Inserting the average score into users table with target_user_id
	UPDATE users SET average_score = avg_score WHERE id = target_user_id;	
END $$
DELIMITER ;
