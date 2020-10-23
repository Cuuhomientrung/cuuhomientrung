cd project
python3 manage.py migrate app 0060_auto_20201023_0623
psql -U 'administrator' -d 'cuuhomientrung' -f app/migrations/sql/cap_nhat_trang_thai_ho_dan.sql
python3 manage.py migrate app 0061_auto_20201023_0823