# Initialize MultiLoc2 setup file
python /webservice/ml2setup.py

# Add cleanup script to cron
crontab -l > current_cron
echo "0 0 * * * sh /webservice/job_cleanup.sh" >> current_cron
crontab current_cron
rm current_cron

/etc/init.d/apache2 start
tail -f /var/log/apache2/error.log
