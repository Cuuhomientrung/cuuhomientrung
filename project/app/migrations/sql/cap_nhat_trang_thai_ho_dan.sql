/*
Create new status in table app_trangthaihodan
*/

INSERT INTO app_trangthaihodan (id, name, created_time, update_time) VALUES 
(1, 'Chưa xác minh', NOW(), NOW()),
(2, 'Không gọi được', NOW(), NOW()),
(3, 'Cần ứng cứu gấp', NOW(), NOW()),
(4, 'Đã gửi cứu hộ', NOW(), NOW()),
(5, 'Cần thức ăn', NOW(), NOW()),
(6, 'Cần thuốc men', NOW(), NOW()),
(7, 'Đã an toàn', NOW(), NOW());

/*
Update app_hodan, set value of status_key_id based on status
*/
UPDATE app_hodan SET status_key_id = 1 WHERE status = 0;
UPDATE app_hodan SET status_key_id = 2 WHERE status = 2;
UPDATE app_hodan SET status_key_id = 3 WHERE status = 1 OR status = 4;
UPDATE app_hodan SET status_key_id = 7 WHERE status = 3;

/*
Update app_hodan, set value of status based on status_key_id
*/
-- UPDATE app_hodan SET status = status_key_id;

