# Databasin Cron Schedule Guide

Complete guide to creating and managing cron expressions for Databasin automation scheduling.

## Overview

Cron expressions are a powerful way to schedule automations to run at specific times or intervals. Databasin uses standard cron syntax to define when your automations should execute, from simple schedules like "every hour" to complex patterns like "every weekday at 9am during Q1 and Q3."

**Use Cases:**

- ETL pipelines that run daily at 2am
- Hourly data synchronization during business hours
- Weekly reports generated every Monday morning
- Monthly cleanup tasks on the first day of each month
- Real-time monitoring that checks every minute

---

## Cron Expression Format

### Standard 5-Field Format

Databasin uses the standard 5-field cron format:

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-7, where 0 and 7 are Sunday)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

### Field Values

| Field        | Allowed Values           | Special Characters  |
| ------------ | ------------------------ | ------------------- |
| Minute       | 0-59                     | `*` `,` `-` `/`     |
| Hour         | 0-23                     | `*` `,` `-` `/`     |
| Day of Month | 1-31                     | `*` `,` `-` `/` `?` |
| Month        | 1-12                     | `*` `,` `-` `/`     |
| Day of Week  | 0-7 (0 and 7 are Sunday) | `*` `,` `-` `/` `?` |

### Special Characters

| Character | Meaning                             | Example                                          |
| --------- | ----------------------------------- | ------------------------------------------------ |
| `*`       | Any value (wildcard)                | `* * * * *` = every minute                       |
| `,`       | Value list separator                | `0,30 * * * *` = top and bottom of every hour    |
| `-`       | Range of values                     | `0 9-17 * * *` = every hour from 9am to 5pm      |
| `/`       | Step values                         | `*/15 * * * *` = every 15 minutes                |
| `?`       | No specific value (day fields only) | Used when specifying day of week OR day of month |

---

## Common Patterns Library

### Every Minute

```
* * * * *
```

**Use Case:** Real-time monitoring, high-frequency data collection
**Warning:** Can be resource-intensive, use sparingly

---

### Every 5 Minutes

```
*/5 * * * *
```

**Use Case:** Near real-time dashboards, frequent status checks

---

### Every 15 Minutes

```
*/15 * * * *
```

**Use Case:** Regular data syncs, periodic health checks
**Runs at:** :00, :15, :30, :45 of every hour

---

### Every 30 Minutes

```
*/30 * * * *
```

**Use Case:** Moderate frequency data updates
**Runs at:** :00 and :30 of every hour

---

### Every Hour (on the hour)

```
0 * * * *
```

**Use Case:** Hourly aggregations, regular updates
**Runs at:** 1:00, 2:00, 3:00, etc.

---

### Every Hour at :30

```
30 * * * *
```

**Use Case:** Hourly tasks offset from the hour
**Runs at:** 1:30, 2:30, 3:30, etc.

---

### Every Day at Midnight

```
0 0 * * *
```

**Use Case:** Daily ETL, end-of-day processing, daily reports
**Runs at:** 12:00am (00:00) every day

---

### Every Day at 2am

```
0 2 * * *
```

**Use Case:** Daily ETL during low-traffic hours
**Runs at:** 2:00am every day
**Note:** Common choice to avoid midnight UTC issues

---

### Every Day at 3am

```
0 3 * * *
```

**Use Case:** Daily batch processing
**Runs at:** 3:00am every day

---

### Every Day at 9am

```
0 9 * * *
```

**Use Case:** Daily reports for morning review
**Runs at:** 9:00am every day

---

### Twice Daily (6am and 6pm)

```
0 6,18 * * *
```

**Use Case:** Morning and evening data syncs
**Runs at:** 6:00am and 6:00pm every day

---

### Every Weekday at 9am

```
0 9 * * 1-5
```

**Use Case:** Business day reports, weekday-only processing
**Runs at:** 9:00am Monday through Friday
**Days:** 1=Monday, 5=Friday

---

### Every Monday at 9am

```
0 9 * * 1
```

**Use Case:** Weekly reports, week-start processing
**Runs at:** 9:00am every Monday

---

### Every Friday at 5pm

```
0 17 * * 5
```

**Use Case:** End-of-week summaries, Friday reports
**Runs at:** 5:00pm (17:00) every Friday

---

### Every Weekend Day at 10am

```
0 10 * * 0,6
```

**Use Case:** Weekend batch processing
**Runs at:** 10:00am Saturday and Sunday
**Days:** 0=Sunday, 6=Saturday

---

### First Day of Month at Midnight

```
0 0 1 * *
```

**Use Case:** Monthly reports, billing cycles, monthly cleanup
**Runs at:** 12:00am on the 1st of every month

---

### First Day of Month at 3am

```
0 3 1 * *
```

**Use Case:** Monthly processing during low-traffic hours
**Runs at:** 3:00am on the 1st of every month

---

### Last Day of Month

```
0 0 28-31 * *
```

**Use Case:** End-of-month processing
**Note:** Not true last day - runs on days 28-31
**Limitation:** Cron cannot detect true last day; use conditional logic in automation

---

### First Monday of Month at 9am

```
0 9 1-7 * 1
```

**Use Case:** Monthly Monday meetings, monthly reports on first Monday
**Explanation:** Runs on Monday (1) if day-of-month is 1-7
**Result:** First Monday of each month

---

### Every Quarter (Jan, Apr, Jul, Oct)

```
0 0 1 1,4,7,10 *
```

**Use Case:** Quarterly reports, quarterly data archival
**Runs at:** 12:00am on January 1, April 1, July 1, October 1

---

### Every Quarter First Business Day

```
0 9 1-7 1,4,7,10 1-5
```

**Use Case:** Quarterly business reports
**Explanation:** First weekday (1-5) in first week (1-7) of quarter months
**Result:** First business day of each quarter

---

### Every 6 Hours

```
0 */6 * * *
```

**Use Case:** Regular throughout-the-day syncs
**Runs at:** 12:00am, 6:00am, 12:00pm, 6:00pm

---

### Every 4 Hours During Business Day

```
0 8,12,16 * * *
```

**Use Case:** Business hours data refreshes
**Runs at:** 8:00am, 12:00pm, 4:00pm

---

### Business Hours Only (9am-5pm, every hour)

```
0 9-17 * * 1-5
```

**Use Case:** Hourly syncs during work hours
**Runs at:** Every hour from 9am to 5pm, Monday through Friday
**Total:** 9 times per weekday

---

### Every 30 Minutes During Business Hours

```
*/30 9-17 * * 1-5
```

**Use Case:** Frequent business-hours updates
**Runs at:** Every 30 minutes from 9:00am to 5:30pm, Monday-Friday

---

### Nightly at 1:30am

```
30 1 * * *
```

**Use Case:** Off-hours batch processing
**Runs at:** 1:30am every day

---

### Every Sunday at 3am

```
0 3 * * 0
```

**Use Case:** Weekly maintenance, weekly backups
**Runs at:** 3:00am every Sunday

---

### Mid-Month Check (15th at Noon)

```
0 12 15 * *
```

**Use Case:** Mid-month reports, bi-monthly processing
**Runs at:** 12:00pm on the 15th of every month

---

### Every 2 Hours

```
0 */2 * * *
```

**Use Case:** Periodic data collection
**Runs at:** 12:00am, 2:00am, 4:00am, 6:00am, etc.

---

### Every 3 Hours Starting at 3am

```
0 3-23/3 * * *
```

**Use Case:** Regular syncs starting mid-night
**Runs at:** 3:00am, 6:00am, 9:00am, 12:00pm, 3:00pm, 6:00pm, 9:00pm

---

### Twice a Week (Tuesday and Thursday at 10am)

```
0 10 * * 2,4
```

**Use Case:** Bi-weekly reports
**Runs at:** 10:00am every Tuesday and Thursday

---

### Every 10 Minutes

```
*/10 * * * *
```

**Use Case:** Frequent monitoring
**Runs at:** :00, :10, :20, :30, :40, :50 of every hour

---

### Working Days at 7am

```
0 7 * * 1-5
```

**Use Case:** Pre-work data preparation
**Runs at:** 7:00am Monday through Friday

---

### Every 20 Minutes

```
*/20 * * * *
```

**Use Case:** Regular but not excessive monitoring
**Runs at:** :00, :20, :40 of every hour

---

## Business Scenarios

### Daily ETL at 2am

```
0 2 * * *
```

**Scenario:** Extract data from source systems, transform, and load into data warehouse
**Why 2am:** Low traffic time, after midnight UTC cutover, before business day
**Considerations:**

- Allow 3-4 hours for completion before business day
- Monitor for long-running jobs
- Consider timezone implications

---

### Hourly Sync During Business Hours

```
0 9-17 * * 1-5
```

**Scenario:** Sync CRM data to analytics platform every hour during work day
**Why this pattern:** Balance freshness with system load
**Considerations:**

- 9 executions per weekday
- No weekend load
- Aligns with business activity

---

### Weekly Reports on Monday Morning

```
0 7 * * 1
```

**Scenario:** Generate weekly summary reports for Monday morning review
**Why 7am Monday:** Ready for start of work week
**Considerations:**

- Runs 52 times per year
- Should complete before 9am meetings
- Data includes full previous week

---

### Monthly Cleanup on 1st

```
0 3 1 * *
```

**Scenario:** Archive old data, purge temp files, compact databases
**Why 3am on 1st:** Start of month, low-traffic hour
**Considerations:**

- 12 executions per year
- May be long-running
- Plan for month-end processing conflicts

---

### Real-Time Monitoring Every Minute

```
* * * * *
```

**Scenario:** Monitor critical API endpoints, check system health
**Warning:** 1,440 executions per day - use judiciously
**Considerations:**

- High resource usage
- Quick execution required (< 60 seconds)
- Consider if truly needed vs. every 5 minutes

---

### Quarterly Financial Reports

```
0 6 1 1,4,7,10 *
```

**Scenario:** Generate quarterly financial summaries
**Why 6am on quarter start:** Early morning, start of new quarter
**Considerations:**

- 4 executions per year
- May need previous quarter data
- Coordinate with fiscal year calendar

---

### End-of-Day Processing at 11pm

```
0 23 * * *
```

**Scenario:** Finalize daily transactions, close daily books
**Why 11pm:** End of business day, before midnight rollover
**Considerations:**

- Completes before midnight
- Captures full business day
- Timezone-aware for global operations

---

### Bi-Weekly Payroll (Every Other Monday)

```
0 8 * * 1
```

**Note:** Cron cannot do "every other week" natively
**Solution:** Run weekly, use conditional logic in automation to check week number
**Alternative:** Use two separate schedules for Week A and Week B dates

---

### Every 15 Minutes During Market Hours

```
*/15 9-16 * * 1-5
```

**Scenario:** Stock market data collection (9am-4pm EST weekdays)
**Considerations:**

- Adjust for market timezone
- Excludes market holidays (needs manual override)
- 32 executions per trading day

---

## Timezone Considerations

### Understanding Timezones

**Critical:** Cron expressions run in the **server timezone**, not the user's local timezone.

### Server Timezone

Databasin automations run in **UTC (Coordinated Universal Time)** by default.

**Example:**

- You want a report at 9am Eastern Time (ET)
- Eastern is UTC-5 (EST) or UTC-4 (EDT)
- Your cron must be: `0 13 * * *` (UTC) or `0 14 * * *` (UTC during EDT)

### Timezone Conversion Table

| Your Local Time    | UTC Time (Winter) | UTC Time (Summer) | Cron Expression |
| ------------------ | ----------------- | ----------------- | --------------- |
| 9:00am EST (UTC-5) | 2:00pm UTC        | -                 | `0 14 * * *`    |
| 9:00am EDT (UTC-4) | -                 | 1:00pm UTC        | `0 13 * * *`    |
| 9:00am PST (UTC-8) | 5:00pm UTC        | -                 | `0 17 * * *`    |
| 9:00am PDT (UTC-7) | -                 | 4:00pm UTC        | `0 16 * * *`    |
| 9:00am CST (UTC-6) | 3:00pm UTC        | -                 | `0 15 * * *`    |
| 9:00am GMT (UTC+0) | 9:00am UTC        | 9:00am UTC        | `0 9 * * *`     |

### Daylight Saving Time (DST) Impacts

**Problem:** DST changes mean your schedule shifts by 1 hour twice a year.

**Solutions:**

1. **Use UTC time** (recommended)
   - Immune to DST changes
   - Predictable year-round
   - May not align with business hours during DST transitions

2. **Accept the shift**
   - Keep local time consistent
   - Update cron twice per year
   - Automation runs at different local times

3. **Use server local timezone if available**
   - Some systems support timezone-aware cron
   - Check Databasin automation settings for timezone options

### Best Practices

**For Global Operations:**

- Use UTC consistently
- Document timezone clearly in automation name/description
- Example: "Daily ETL at 06:00 UTC (2am EST / 11pm PST)"

**For Single-Timezone Operations:**

- Calculate UTC offset
- Update cron expressions during DST transitions
- Set calendar reminders for DST change dates

**For Multi-Region Operations:**

- Create separate automations per region
- Use region-specific UTC offsets
- Example: "EU Daily Report (UTC+1)" and "US Daily Report (UTC-5)"

---

## Testing Cron Expressions

### Online Validators

**Recommended Tools:**

1. **crontab.guru**
   - URL: https://crontab.guru
   - Features: Simple, clean, explains schedule in plain English
   - Best for: Quick validation and learning

2. **Crontab Generator**
   - URL: https://crontab-generator.org
   - Features: Interactive builder, shows next run times
   - Best for: Building complex expressions

3. **CronJobs Schedule Editor**
   - URL: https://cronjob.xyz
   - Features: Visual editor, timezone support
   - Best for: Timezone-aware scheduling

### How to Test Before Deploying

**Step 1: Validate Syntax**

```bash
# Use an online validator or local cron checker
echo "0 9 * * 1-5" | crontab-checker
```

**Step 2: Check Next Execution Times**
Use crontab.guru or similar to see next 5-10 execution times.

**Example:**

- Expression: `0 9 * * 1-5`
- Next runs: Monday 9am, Tuesday 9am, Wednesday 9am, Thursday 9am, Friday 9am

**Step 3: Verify Timezone**

- Confirm server timezone (UTC for Databasin)
- Convert your desired local time to server time
- Validate the UTC cron expression

**Step 4: Dry Run**

- Create automation with cron schedule
- Set to "test mode" or minimal execution
- Monitor first few executions
- Verify timing matches expectations

**Step 5: Review Execution History**
After deployment:

- Check automation execution logs
- Verify timestamps match expected schedule
- Look for missed or duplicate executions

### Manual Testing

**Create a Test Automation:**

```json
{
	"automationName": "CRON_TEST_Every_5_Min",
	"automationScheduleType": "cron",
	"automationSchedule": "*/5 * * * *",
	"automationEnabled": true,
	"tasks": [
		{
			"taskType": "notebook",
			"taskName": "Log current time",
			"taskOrder": 1,
			"notebookId": 123
		}
	]
}
```

**Monitor for 1 hour:**

- Should execute 12 times (every 5 minutes)
- Verify timing is consistent
- Check for any gaps or irregularities

---

## Common Mistakes

### 1. Forgetting Asterisks

**Wrong:**

```
0 9
```

**Correct:**

```
0 9 * * *
```

**Error:** Incomplete cron expression, missing day/month/weekday fields.

---

### 2. Day vs Month Field Order Confusion

**Wrong:**

```
0 9 1 * 15
```

**Intended:** 9am on the 15th of every month
**Actual:** 9am on January 1st, every year (month 1, any day, weekday 15 - invalid)

**Correct:**

```
0 9 15 * *
```

**Explanation:** Day-of-month is field 3, not field 5.

---

### 3. Wrong Field Order

**Wrong:**

```
9 0 * * *
```

**Intended:** 9am daily
**Actual:** 12:09am daily (minute 9, hour 0)

**Correct:**

```
0 9 * * *
```

**Explanation:** Hour comes before minute? No! Minute is field 1, hour is field 2.

---

### 4. Timezone Assumptions

**Wrong:**

```
0 9 * * *
```

**Assumption:** Runs at 9am in my local time
**Reality:** Runs at 9am **UTC** (may be 4am or 2am local time)

**Correct:**

```
0 14 * * *
```

**For 9am EST (UTC-5):** Use 14:00 UTC (2pm UTC = 9am EST)

---

### 5. Using 24 for Midnight

**Wrong:**

```
0 24 * * *
```

**Error:** Hour field only accepts 0-23

**Correct:**

```
0 0 * * *
```

**Explanation:** Midnight is hour 0, not hour 24.

---

### 6. Day of Week Starting at 1

**Wrong:**

```
0 9 * * 1
```

**Assumption:** Sunday is 1
**Reality:** Sunday is **0** (or 7), Monday is 1

**Correct for Sunday:**

```
0 9 * * 0
```

**Correct for Monday:**

```
0 9 * * 1
```

---

### 7. Too Frequent Execution

**Problematic:**

```
* * * * *
```

**Issue:** Runs 1,440 times per day (every minute)
**Impact:** High resource usage, potential system overload

**Better:**

```
*/5 * * * *
```

**Result:** Runs 288 times per day (every 5 minutes) - 80% reduction

---

### 8. Last Day of Month Attempt

**Wrong:**

```
0 0 31 * *
```

**Intended:** Last day of every month
**Actual:** Only runs in months with 31 days (skips Feb, Apr, Jun, Sep, Nov)

**Workaround:**

```
0 0 28-31 * *
```

**Result:** Runs on days 28-31 (includes last day, but also runs on 28-30)
**Note:** Requires conditional logic in automation to detect true last day.

---

### 9. Comma vs Dash Confusion

**Wrong:**

```
0 9 1,5 * *
```

**Intended:** Weekdays (Monday-Friday)
**Actual:** 1st and 5th of every month (day-of-month field)

**Correct for Weekdays:**

```
0 9 * * 1-5
```

**Correct for 1st and 5th:**

```
0 9 1,5 * *
```

---

### 10. Step Syntax Errors

**Wrong:**

```
/15 * * * *
```

**Error:** Missing starting value before `/`

**Correct:**

```
*/15 * * * *
```

**Result:** Every 15 minutes (0, 15, 30, 45)

**Also Correct:**

```
0/15 * * * *
```

**Result:** Same as above - every 15 minutes starting at :00

---

### 11. Range Misconceptions

**Wrong:**

```
0 9-17 * * *
```

**Assumption:** Runs once between 9am and 5pm
**Actual:** Runs **every hour** from 9am to 5pm (9 times)

**Correct for once daily at 9am:**

```
0 9 * * *
```

---

### 12. Both Day Fields Specified

**Problematic:**

```
0 9 15 * 1
```

**Intended:** 9am on the 15th if it's a Monday
**Actual:** 9am on **either** the 15th **OR** every Monday

**Explanation:** When both day-of-month and day-of-week are specified (not `*` or `?`), they create an OR condition, not AND.

**Solution:** Use conditional logic in automation task or script to check both conditions.

---

## Troubleshooting

### Automation Not Running at Expected Time

**Symptom:** Automation doesn't execute when you expect it to.

**Checklist:**

1. **Verify Cron Expression**
   - Use crontab.guru to validate
   - Check field order (minute, hour, day, month, weekday)
   - Ensure all 5 fields are present

2. **Check Timezone**
   - Confirm server runs in UTC
   - Convert your local time to UTC
   - Account for DST if applicable

3. **Verify Automation is Enabled**
   - Check `automationEnabled: true`
   - Look for manual disable events in logs

4. **Check Execution History**
   - Review automation logs
   - Look for errors during previous runs
   - Check if automation is stuck

5. **Validate Date/Time Fields**
   - Ensure day-of-month exists (no Feb 30th)
   - Check month numbers (1-12, not 0-11)
   - Verify weekday numbers (0-7)

**Example Debug:**

```
Expression: 0 9 * * *
Expected: 9am local time
Actual: Not running
Problem: Server is UTC, local time is EST (UTC-5)
Solution: Change to 0 14 * * * (9am EST = 2pm UTC)
```

---

### Running Too Frequently

**Symptom:** Automation runs more often than intended.

**Common Causes:**

1. **Missing Fields**

   ```
   Wrong: */5 * *
   Correct: */5 * * * *
   ```

2. **Wildcard Instead of Specific Value**

   ```
   Wrong: * 9 * * * (every minute during 9am hour)
   Correct: 0 9 * * * (only at 9:00am)
   ```

3. **Step Syntax Misunderstanding**

   ```
   Wrong: */1 * * * * (every minute - 1,440/day)
   Intended: Every hour
   Correct: 0 * * * * (every hour - 24/day)
   ```

4. **Range Misuse**
   ```
   Wrong: 0 9-17 * * * (every hour 9am-5pm - 9x/day)
   Intended: Once during business hours
   Correct: 0 9 * * * (once at 9am)
   ```

**Solution:**

- Review each field carefully
- Test with online validator
- Check execution logs for frequency
- Calculate expected executions per day/week

---

### Skipping Executions

**Symptom:** Automation misses scheduled runs.

**Possible Causes:**

1. **Long-Running Previous Execution**
   - If automation takes longer than schedule interval
   - Example: Every 5 minutes, but task takes 10 minutes
   - **Solution:** Increase interval or optimize task

2. **System Maintenance**
   - Server downtime during scheduled time
   - **Solution:** Review maintenance windows, adjust schedule

3. **Resource Constraints**
   - System too busy to start new execution
   - **Solution:** Spread out schedules, increase resources

4. **Invalid Date**

   ```
   Expression: 0 0 31 2 *
   Problem: February never has 31 days
   Solution: Use 0 0 28 2 * for Feb 28th
   ```

5. **DST Transition**
   - "Spring forward" skips 2am-3am hour
   - **Solution:** Avoid scheduling during DST transition hours

**Debugging Steps:**

1. Check system logs for errors
2. Review execution history for gaps
3. Monitor system resources during scheduled time
4. Verify cron expression doesn't target invalid dates
5. Consider race conditions with dependencies

---

### Timezone Debugging

**Symptom:** Automation runs at wrong time of day.

**Debugging Process:**

**Step 1: Confirm Server Timezone**

```bash
# If you have server access
date
timedatectl
```

**Step 2: Calculate UTC Offset**

- Find your timezone's UTC offset
- EST = UTC-5, EDT = UTC-4
- PST = UTC-8, PDT = UTC-7
- GMT = UTC+0

**Step 3: Convert Local to UTC**
| Local Time | Timezone | UTC Offset | UTC Time |
|------------|----------|------------|----------|
| 9:00am | EST | -5 | 2:00pm (14:00) |
| 9:00am | PST | -8 | 5:00pm (17:00) |
| 5:00pm | EST | -5 | 10:00pm (22:00) |

**Step 4: Update Cron Expression**

```
Local: 9:00am EST
UTC: 2:00pm (14:00)
Cron: 0 14 * * *
```

**Step 5: Test and Verify**

- Create test automation
- Monitor first execution
- Verify timestamp in logs matches expected local time

**DST Considerations:**

- Set reminders for DST transitions (March and November)
- Update cron expressions if you want consistent local time
- Document whether schedule follows DST or UTC

---

### Day of Week vs Day of Month Conflicts

**Symptom:** Automation runs on unexpected days.

**Problem:**

```
0 9 15 * 1
```

**Intended:** 9am on the 15th, only if it's a Monday
**Actual:** 9am on the 15th **OR** 9am on every Monday

**Explanation:** When both day-of-month and day-of-week are specified (not `*` or `?`), cron uses **OR** logic, not AND.

**Solutions:**

**Option 1: Use Only One Day Field**

```
# Every Monday, regardless of date
0 9 * * 1

# 15th of every month, regardless of day of week
0 9 15 * *
```

**Option 2: Use Conditional Logic in Automation**

```
# Run every Monday
0 9 * * 1

# In automation task, check:
# if (day_of_month == 15) then execute
```

**Option 3: Create Specific Schedules**

```
# If pattern is predictable, create multiple schedules
# Example: First Monday of month
0 9 1-7 * 1
```

---

## Quick Reference Card

### Cron Syntax Reminder

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of Week (0-7, 0 and 7 are Sunday)
│ │ │ └─────── Month (1-12)
│ │ └───────────── Day of Month (1-31)
│ └─────────────────── Hour (0-23)
└───────────────────────── Minute (0-59)
```

### Most Common Patterns

| Pattern                    | Cron Expression    | Description      |
| -------------------------- | ------------------ | ---------------- |
| Every minute               | `* * * * *`        | 1,440 times/day  |
| Every 5 minutes            | `*/5 * * * *`      | 288 times/day    |
| Every 15 minutes           | `*/15 * * * *`     | 96 times/day     |
| Every 30 minutes           | `*/30 * * * *`     | 48 times/day     |
| Every hour                 | `0 * * * *`        | 24 times/day     |
| Every day at midnight      | `0 0 * * *`        | Daily at 00:00   |
| Every day at 2am           | `0 2 * * *`        | Daily at 02:00   |
| Every day at 9am           | `0 9 * * *`        | Daily at 09:00   |
| Every weekday at 9am       | `0 9 * * 1-5`      | Mon-Fri at 09:00 |
| Every Monday at 9am        | `0 9 * * 1`        | Weekly on Monday |
| First of month at midnight | `0 0 1 * *`        | Monthly on 1st   |
| Every quarter              | `0 0 1 1,4,7,10 *` | 4 times/year     |

### Special Character Quick Lookup

| Character | Meaning       | Example                         |
| --------- | ------------- | ------------------------------- |
| `*`       | Every/Any     | `* * * * *` = every minute      |
| `*/n`     | Every n units | `*/15 * * * *` = every 15 min   |
| `n-m`     | Range         | `0 9-17 * * *` = 9am-5pm hourly |
| `n,m`     | List          | `0 9,17 * * *` = 9am and 5pm    |
| `?`       | No value      | Rarely needed in standard cron  |

### Timezone Conversion Cheat Sheet

**For 9:00am Local Time:**

| Your Timezone | Cron Expression (Winter) | Cron Expression (Summer) |
| ------------- | ------------------------ | ------------------------ |
| EST (UTC-5)   | `0 14 * * *`             | `0 13 * * *`             |
| CST (UTC-6)   | `0 15 * * *`             | `0 14 * * *`             |
| MST (UTC-7)   | `0 16 * * *`             | `0 15 * * *`             |
| PST (UTC-8)   | `0 17 * * *`             | `0 16 * * *`             |
| GMT (UTC+0)   | `0 9 * * *`              | `0 9 * * *`              |
| CET (UTC+1)   | `0 8 * * *`              | `0 7 * * *`              |

### Common Mistake Checklist

- [ ] All 5 fields present (minute, hour, day, month, weekday)
- [ ] Fields in correct order
- [ ] Hour is 0-23 (not 1-24)
- [ ] Midnight is `0` not `24`
- [ ] Sunday is `0` or `7` (not `1`)
- [ ] Month is 1-12 (not 0-11)
- [ ] Timezone accounted for (local vs UTC)
- [ ] Step syntax includes `*` before `/` (e.g., `*/15`)
- [ ] Day/month values exist (no Feb 30, no month 13)
- [ ] Frequency is intentional (not accidentally every minute)

### Testing Checklist

- [ ] Validate syntax on crontab.guru
- [ ] Check next 5+ execution times
- [ ] Convert local time to UTC
- [ ] Account for DST if applicable
- [ ] Create test automation
- [ ] Monitor first 3-5 executions
- [ ] Verify logs show correct timestamps
- [ ] Confirm execution frequency matches intent

---

## Additional Resources

### Online Tools

- **crontab.guru** - https://crontab.guru - Best for quick validation
- **Crontab Generator** - https://crontab-generator.org - Interactive builder
- **CronJobs.io** - https://cronjob.xyz - Timezone-aware editor

### Databasin Documentation

- Automation API Reference: `@api-reference.md`
- Automation Examples: `@examples.md`
- Task Types Guide: `@task-types-guide.md` (coming soon)

### Cron Standards

- POSIX Cron: Original Unix cron specification
- Vixie Cron: Most common implementation (used by Linux)
- Quartz Cron: Extended format with seconds (not used by Databasin)

---

## Summary

**Key Takeaways:**

1. **Format:** 5 fields (minute, hour, day, month, weekday)
2. **Timezone:** Databasin runs in UTC - convert local time accordingly
3. **Testing:** Always validate with crontab.guru before deployment
4. **Common Patterns:** Use the library above as copy-paste templates
5. **Mistakes:** Watch for field order, timezone, and wildcard confusion
6. **DST:** Plan for twice-yearly schedule adjustments if needed

**Best Practices:**

- Document timezone in automation name/description
- Test with dry runs before production deployment
- Monitor first few executions after creating schedule
- Use step syntax (`*/n`) for regular intervals
- Avoid over-frequent schedules (every minute) unless truly necessary
- Keep cron expressions simple and readable
- Review execution logs regularly for missed or duplicate runs

**When in Doubt:**

- Start with a common pattern from this guide
- Test in a sandbox/dev environment first
- Verify timing with execution logs
- Adjust based on observed behavior

---

_For questions or issues with cron scheduling in Databasin automations, consult the automation API reference or contact support._
