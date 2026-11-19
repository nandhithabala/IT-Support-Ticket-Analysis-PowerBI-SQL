-- 1. Average Resolution Time & Ticket Count by Priority Level
SELECT 
    priority,
    COUNT(ticket_id) AS total_tickets,
    ROUND(AVG(CAST(resolution_time_hours AS REAL)), 2) AS avg_resolution_hours
FROM tickets
WHERE resolution_time_hours IS NOT NULL AND resolution_time_hours != ''
GROUP BY priority
ORDER BY avg_resolution_hours ASC;

-- 2. Top Recurring Technical Issues (Product Area & Issue Type)
SELECT 
    product_area,
    issue_type,
    COUNT(ticket_id) AS issue_count,
    ROUND(AVG(CAST(resolution_time_hours AS REAL)), 2) AS avg_hours_to_resolve
FROM tickets
GROUP BY product_area, issue_type
ORDER BY issue_count DESC;

-- 3. SLA Plan & Resolution Status Performance (Including CSAT & Reopened Rate)
SELECT 
    sla_plan,
    status,
    COUNT(ticket_id) AS ticket_count,
    ROUND(AVG(csat_score), 2) AS avg_csat,
    SUM(reopened) AS total_reopened
FROM tickets
GROUP BY sla_plan, status
ORDER BY sla_plan, ticket_count DESC;

-- 4. Monthly Ticket Volume & Sentiment Breakdown
SELECT 
    SUBSTR(created_at, 1, 7) AS ticket_month,
    COUNT(ticket_id) AS total_tickets,
    ROUND(AVG(CAST(resolution_time_hours AS REAL)), 2) AS avg_resolution_hours
FROM tickets
GROUP BY ticket_month
ORDER BY ticket_month ASC;

-- 5. Regional & Platform Ticket Distribution
SELECT 
    region,
    platform,
    COUNT(ticket_id) AS total_tickets
FROM tickets
GROUP BY region, platform
ORDER BY total_tickets DESC;
