CREATE DATABASE IF NOT EXISTS MoodDb DEFAULT CHARACTER SET utf8;

USE `MoodDb`;
CREATE TABLE IF NOT EXISTS `tblUser` (
`Id` INT NOT NULL AUTO_INCREMENT,
`Name` VARCHAR(45) NOT NULL,
`Slug` VARCHAR(45) NULL,
`Email` VARCHAR(45) NOT NULL,
`CREATED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`CREATED_BY` INT NULL,
`MODIFIED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`MODIFIED_BY` INT NULL,
PRIMARY KEY (`Id`));


CREATE TABLE IF NOT EXISTS `tblTeam` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `Slug` VARCHAR(45) NULL,
  `Description`VARCHAR(45) NULL,
  `CREATED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CREATED_BY` INT NULL,
  `MODIFIED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `MODIFIED_BY` INT NULL,
PRIMARY KEY (`Id`));


CREATE TABLE IF NOT EXISTS `tblMood` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Timestamp` INT(20) NOT NULL,
  `Label` VARCHAR(45) NOT NULL,
  `Value` INT NOT NULL,
  `User_Id` INT NOT NULL,
  `CREATED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CREATED_BY` INT NULL,
  `MODIFIED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `MODIFIED_BY` INT NULL,
CONSTRAINT mood_pk PRIMARY KEY (`Id`),
CONSTRAINT user_pk FOREIGN KEY (`User_Id`)
  REFERENCES tblUser(Id)
  ON UPDATE CASCADE ON DELETE RESTRICT );


CREATE TABLE IF NOT EXISTS `tblSnippet` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Timestamp` INT(20) NOT NULL,
  `Content` VARCHAR(1000) NOT NULL,
  `User_Id` INT NOT NULL,
  `CREATED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CREATED_BY` INT NULL,
  `MODIFIED_ON` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `MODIFIED_BY` INT NULL,
CONSTRAINT snippet_pk PRIMARY KEY (`Id`),
CONSTRAINT user_id FOREIGN KEY (`User_Id`)
  REFERENCES tblUser (Id)
  ON UPdATE CASCADE ON DELETE RESTRICT );


# Team User Map

CREATE TABLE IF NOT EXISTS `User_Team_Map` (
  `User_Id` int NOT NULL,
  `Team_Id` int NOT NULL,
  PRIMARY KEY (`User_Id`,`Team_Id`),
  FOREIGN KEY (`User_Id`) REFERENCES `tblUser` (`Id`),
  FOREIGN KEY (`Team_Id`) REFERENCES `tblTeam` (`Id`)
);



USE `MoodDb`;

# Create User

DROP procedure IF EXISTS `spCreateUser`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spCreateUser` (
IN p_name varchar(50) CHARSET utf8,
IN p_slug varchar(50),
IN p_email varchar(50)
)
BEGIN

if ( select exists (select 1 from tblUser where Email = p_email) ) THEN
  SELECT 'Username Exists !!';
ELSE

insert into tblUser
(
    Name,
    Slug,
    Email
)
values
(
    p_name,
    p_slug,
    p_email
);

END IF;
END$$
DELIMITER ;

# Update User

DROP PROCEDURE IF EXISTS `spUpdateUser`;
DELIMITER $$
USE `MoodDb` $$
CREATE PROCEDURE `spUpdateUser` (
  IN p_name varchar(50) CHARSET utf8,
  IN p_slug varchar(50),
  IN p_email varchar(50)
)
BEGIN

if ( select exists (select 1 from tblUser where Email = p_email) ) THEN
  UPDATE tblUser SET
    Name = p_name,
    Slug = p_slug
  WHERE Email = p_email;
ELSE
  SELECT 'User does not exist !!';
END IF;
END$$
DELIMITER ;

# Get User

DROP procedure IF EXISTS `spGetUser`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetUser` (
  IN p_id int
)
  BEGIN
    SELECT Id, Name FROM tblUser WHERE Id = p_id;
  END$$

DELIMITER ;


# Get Users

DROP procedure IF EXISTS `spGetUsers`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetUsers` (
  IN p_slug VARCHAR(45)
)
  BEGIN
    IF p_slug IS NULL THEN
      SELECT Id, Name, Slug, Email FROM tblUser LIMIT 20;
    ELSE
      SELECT Id, Name, Slug, Email FROM tblUser where Slug = p_slug;
    END IF;
  END$$

DELIMITER ;

# Delete User

DROP procedure IF EXISTS `spDeleteUser`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spDeleteUser` (
IN p_id INT
)
  BEGIN
    DELETE FROM tblUser WHERE Id = p_id;
  END$$

DELIMITER ;

# Team

# Create Team

DROP procedure IF EXISTS `spCreateTeam`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spCreateTeam` (
  IN p_name varchar(50) CHARSET utf8,
  IN p_slug varchar(50),
  IN p_description varchar(50)
)
BEGIN

  if ( select exists (select 1 from tblTeam where Description = p_description) ) THEN
    SELECT 'Team name Exists !!';
  ELSE

  insert into tblTeam
  (
    Name,
    Slug,
    Description
  )
  values
    (
      p_name,
      p_slug,
      p_description
    );

  END IF;

END$$

DELIMITER ;

# Update Team

DROP PROCEDURE IF EXISTS `spUpdateTeam`;
DELIMITER $$
USE `MoodDb` $$
CREATE PROCEDURE `spUpdateTeam` (
  IN p_id INT,
  IN p_name varchar(50) CHARSET utf8,
  IN p_slug varchar(50),
  IN p_description varchar(50)
)
BEGIN

if ( select exists (select 1 from tblTeam where Id = p_id) ) THEN
  UPDATE tblTeam SET
    Name = p_name,
    Slug = p_slug,
    Description = p_description
  WHERE Id = p_id;
ELSE
  SELECT 'Team does not exist !!';
END IF;
END$$
DELIMITER ;

# Get Teams

DROP procedure IF EXISTS `spGetTeams`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetTeams` ()
  BEGIN
    SELECT Id, Name, Slug, Description FROM tblTeam;
  END$$

DELIMITER ;


# Delete Team

DROP procedure IF EXISTS `spDeleteTeam`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spDeleteTeam` (
  IN p_id INT
)
  BEGIN
    DELETE FROM tblTeam WHERE Id = p_id;
  END$$

DELIMITER ;

# Create Mood

DROP procedure IF EXISTS `spCreateMood`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spCreateMood` (
  IN p_timestamp INT,
  IN p_label VARCHAR(50),
  IN p_value INT,
  IN p_user_id INT
)
BEGIN

if ( select exists (select 1 from tblMood where Timestamp = p_timestamp and User_Id = p_user_id) ) THEN
  SELECT 'Mood exists !!';
ELSE
  insert into tblMood
  (
    Timestamp,
    Label,
    Value,
    User_Id
  )
  values
    (
      p_timestamp,
      p_label,
      p_value,
      p_user_id
    );

END IF;

END$$

DELIMITER ;

# Update Mood

DROP PROCEDURE IF EXISTS `spUpdateMood`;
DELIMITER $$
USE `MoodDb` $$
CREATE PROCEDURE `spUpdateMood` (
  IN p_id INT,
  IN p_timestamp INT,
  IN p_label VARCHAR(50),
  IN p_value INT,
  IN p_user_id INT
)
BEGIN
  if ( select exists (select 1 from tblMood where Timestamp = p_timestamp and User_Id = p_user_id) ) THEN
    UPDATE tblMood SET
      Label = p_label,
      Value = p_value
    WHERE Timestamp = p_timestamp AND User_Id = p_user_id;
  ELSE
    SELECT 'Mood does not exist !!';
  END IF;
END$$
DELIMITER ;

# Get Moods

DROP procedure IF EXISTS `spGetMoods`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetMoods` (
  IN p_start INT,
  IN p_end INT,
  IN p_user_id INT
)
BEGIN
  SELECT Id, Timestamp, Label, Value FROM tblMood
    WHERE User_Id = p_user_id AND Timestamp >= p_start AND Timestamp <= p_end;
END$$

DELIMITER ;

# Delete Mood

DROP procedure IF EXISTS `spDeleteMood`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spDeleteMood` (
  IN p_id INT
)
  BEGIN
    DELETE FROM tblMood WHERE Id = p_id;
  END$$

DELIMITER ;


# Create Snippet

DROP procedure IF EXISTS `spCreateSnippet`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spCreateSnippet` (
  IN p_timestamp INT,
  IN p_content VARCHAR(1000),
  IN p_user_id INT
)
  BEGIN

    if ( select exists (select 1 from tblSnippet where Timestamp = p_timestamp and User_Id = p_user_id) ) THEN
      SELECT 'Snippet exists !!';
    ELSE
      insert into tblSnippet
      (
        Timestamp,
        Content,
        User_Id
      )
      values
        (
          p_timestamp,
          p_content,
          p_user_id
        );
    END IF;
  END$$
DELIMITER ;

# Update Snippet

DROP PROCEDURE IF EXISTS `spUpdateSnippet`;
DELIMITER $$
USE `MoodDb` $$
CREATE PROCEDURE `spUpdateSnippet` (
  IN p_id INT,
  IN p_timestamp INT,
  IN p_content VARCHAR(1000),
  IN p_user_id INT
)
  BEGIN
    if ( select exists (select 1 from tblSnippet where Timestamp = p_timestamp and User_Id = p_user_id) ) THEN
      UPDATE tblSnippet SET
        Content = p_content
      WHERE Timestamp = p_timestamp AND User_Id = p_user_id;
    ELSE
      SELECT 'Snippet does not exist !!';
    END IF;
  END$$
DELIMITER ;

# Get Snippets

DROP procedure IF EXISTS `spGetSnippets`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetSnippets` (
  IN p_start INT,
  IN p_end INT,
  IN p_user_id INT
)
  BEGIN
    SELECT Id, Timestamp, Content FROM tblSnippet
    WHERE User_Id = p_user_id AND Timestamp >= p_start AND Timestamp <= p_end;
  END$$

DELIMITER ;

# Delete Snippet

DROP procedure IF EXISTS `spDeleteSnippet`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spDeleteSnippet` (
  IN p_id INT
)
  BEGIN
    DELETE FROM tblSnippet WHERE Id = p_id;
  END$$

DELIMITER ;


# Get Users per team
DROP procedure IF EXISTS `spGetUsersPerTeam`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spGetUsersPerTeam` (
  IN p_team_id INT
)
  BEGIN
    SELECT Id, Name FROM tblUser A, User_Team_Map B WHERE B.User_Id = A.Id AND B.Team_Id = p_team_id;
  END$$

DELIMITER ;

# Add a user to a team
DROP procedure IF EXISTS `spCreateMembership`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spCreateMembership` (
  IN p_team_id INT,
  IN p_user_id INT
)
  BEGIN
    INSERT INTO User_Team_Map (Team_Id, User_Id) VALUES (p_team_id, p_user_id);
  END $$

DELIMITER ;

# Delete a user to a team
DROP procedure IF EXISTS `spDeleteMembership`;

DELIMITER $$
USE `MoodDb`$$
CREATE PROCEDURE `spDeleteMembership` (
  IN p_team_id INT,
  IN p_user_id INT
)
  BEGIN
    DELETE FROM User_Team_Map WHERE Team_Id = p_team_id AND User_Id = p_user_id;
  END $$

DELIMITER ;
