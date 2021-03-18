CREATE DEFINER=`root`@`localhost` PROCEDURE `pupa`(ye varchar(16),mn varchar(16))

BEGIN

declare done integer default 0;
declare car,send varchar(16);
declare `data` date;
declare pep integer;
declare C1 cursor for

select reg_num, company, `date`, count(company) as pep
from ttn join client using(id_dog)
where YEAR(`date`)=ye AND MONTH(`date`)=mn
group by reg_num
order by company;

declare exit handler for sqlstate '02000' set done=1;
open C1;

while done=0 do
fetch C1 into car,send,`data`,pep;
insert f_table(f_id,f_car,f_send,f_year,f_month,f_ezd)
values(NULL,car,send,ye,mn,pep);
end while;
close C1;
END