-- description: <This trigger will check if the time is update forward>

PRAGMA foreign_keys = ON;

drop trigger if exists TimeMoveForward;
create trigger TimeMoveForward
before update of currentTime on CurrentTime
when ( new.currentTime <= 
		(
			select max(c.currentTime)
			from CurrentTime as c
		) 
	)
begin
	select raise(rollback, 'The time can only advance forward in time');
end;
