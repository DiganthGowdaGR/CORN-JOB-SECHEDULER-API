# Cron Schedule Examples

## Format: `minute hour day month day_of_week`

### Common Schedules:

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every minute | `* * * * *` | Runs every minute |
| Every 5 minutes | `*/5 * * * *` | Every 5 minutes |
| Every hour | `0 * * * *` | At minute 0 of every hour |
| Daily at 9 AM | `0 9 * * *` | Every day at 9:00 AM |
| Weekly (Monday 9 AM) | `0 9 * * 1` | Every Monday at 9 AM |
| Monthly (1st at midnight) | `0 0 1 * *` | First day of month at midnight |
| Weekdays at 2 PM | `0 14 * * 1-5` | Monday to Friday at 2 PM |
| Weekend mornings | `0 10 * * 6,0` | Saturday and Sunday at 10 AM |

### Advanced Examples:

- `30 14 * * *` - Every day at 2:30 PM
- `0 */6 * * *` - Every 6 hours
- `15 2 * * 0` - Every Sunday at 2:15 AM
- `0 9-17 * * 1-5` - Every hour from 9 AM to 5 PM, weekdays only
- `*/10 9-17 * * *` - Every 10 minutes during business hours (9 AM - 5 PM)

### Special Characters:

- `*` = Any value
- `*/n` = Every n units
- `n-m` = Range from n to m
- `n,m` = Specific values n and m