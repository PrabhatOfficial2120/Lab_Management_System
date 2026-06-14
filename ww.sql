



CREATE TRIGGER 'Student-System' 
BEFORE INSERT ON 'Student' 
WHEN ( SELECT count(*) FROM  'Student', 'Batch' WHERE 'Batch.bid'= 'Student.s_id') > 25 
BEGIN 
INSERT INTO 'System' 
WHERE 'sys.id'= ( SELECT count(*) FROM 'System')+1; 
END
