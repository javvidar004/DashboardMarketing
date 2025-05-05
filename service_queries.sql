
SELECT entretaiment.entertainment_id AS entertainment_id, entretaiment.entertainment_name AS name, COUNT(preferred_content_id) AS people
FROM entretaiment, users
WHERE preferred_content_id = entretaiment.entertainment_id
GROUP BY entretaiment.entertainment_id;

SELECT countries.country_id, countries.country_name, ROUND(SUM(users.monthly_spent_entertain),2) AS total_spent
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY countries.country_id, countries.country_name
ORDER BY total_spent DESC;

SELECT countries.country_id, countries.country_name, ROUND(AVG(users.monthly_income),2) AS avg_income
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY countries.country_id, countries.country_name
ORDER BY avg_income DESC;

SELECT countries.country_id, countries.country_name, social_media.socialm_name AS Platform,
CASE
WHEN users.age BETWEEN 0 AND 17 THEN '0-17'
WHEN users.age BETWEEN 18 AND 25 THEN '18-25'
WHEN users.age BETWEEN 26 AND 35 THEN '26-35'
WHEN users.age BETWEEN 36 AND 50 THEN '36-50'
ELSE '51+'
END AS age_group,
COUNT(*) AS total_users
FROM users
JOIN countries ON users.country_id = countries.country_id
JOIN social_media ON users.primary_plat_id = social_media.socialm_id
GROUP BY countries.country_name, social_media.socialm_name, age_group, countries.country_id
ORDER BY countries.country_name, social_media.socialm_name, total_users DESC;

SELECT occupations.occupation_id, occupations.occupation_name, ROUND(SUM(users.monthly_spent_entertain),2) AS total_spent
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
GROUP BY occupations.occupation_name, occupations.occupation_id
ORDER BY total_spent DESC;

SELECT occupations.occupation_name, media_goal.goal_name, COUNT(*) AS total_users
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
JOIN media_goal ON users.primary_sm_goal_id = media_goal.goal_id
GROUP BY occupations.occupation_name, media_goal.goal_name
ORDER BY occupations.occupation_name, total_users DESC;

SELECT
devices.device_name,
COUNT(*) AS total_users
FROM users
JOIN devices ON users.device_sm_id = devices.device_id
GROUP BY devices.device_name
ORDER BY total_users DESC;

SELECT
devices.device_name,
COUNT(*) AS total_users
FROM users
JOIN devices ON users.devide_for_entertainment_id = devices.device_id
GROUP BY devices.device_name
ORDER BY total_users DESC;

SELECT country_name, AVG(users.monthly_income) AS prom_ingresos, AVG(users.monthly_spent_entertain) AS prom_gastos
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY country_name
ORDER BY prom_gastos DESC;

SELECT countries.country_name, AVG(users.d_sm_time) AS prom_redes_sociales, AVG(users.d_entertain_time) AS prom_plat_entret
FROM users
JOIN countries ON users.country_id = countries.country_id
GROUP BY countries.country_name
ORDER BY prom_redes_sociales DESC;

SELECT occupations.occupation_name, social_media.socialm_name,
COUNT(users.user_id) AS total_usuarios
FROM users
JOIN occupations ON users.occupation_id = occupations.occupation_id
JOIN social_media ON users.primary_plat_id = social_media.socialm_id
GROUP BY occupations.occupation_name, social_media.socialm_name
ORDER BY total_usuarios DESC;

SELECT
CASE
WHEN screen_time < 3 THEN 'Bajo'
WHEN screen_time BETWEEN 3 AND 6 THEN 'Moderado'
ELSE 'Alto'
END AS screen_usage,
CASE
WHEN sleep_quality >= 7 THEN 'Buena'
WHEN sleep_quality BETWEEN 5 AND 6 THEN 'Regular'
ELSE 'Mala'
END AS sleep_category,
COUNT(*) AS users_count
FROM users
GROUP BY screen_usage, sleep_category
ORDER BY users_count DESC;

SELECT COUNT(*) AS total_users FROM users;

SELECT c.country_name, COUNT(u.user_id) AS total
FROM users u
JOIN countries c ON u.country_id = c.country_id
GROUP BY c.country_name
ORDER BY total DESC
LIMIT 10;

SELECT d.device_name, COUNT(u.user_id) AS total
FROM users u
JOIN devices d ON u.device_sm_id = d.device_id
GROUP BY d.device_name
ORDER BY total DESC;

SELECT g.gender, COUNT(u.user_id) AS total
FROM users u
JOIN gender g ON u.gender_id = g.gender_id
GROUP BY g.gender;

SELECT o.occupation_name, COUNT(u.user_id) AS total
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
GROUP BY o.occupation_name
ORDER BY total DESC
LIMIT 5;

SELECT o.occupation_name, COUNT(u.user_id) as total
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
GROUP BY o.occupation_name
ORDER BY total DESC
LIMIT 10;

SELECT
    o.occupation_name,
    c.country_name,
    u.tech_savviness_level,
    ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
    COUNT(u.user_id) as user_count
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
JOIN countries c ON u.country_id = c.country_id
WHERE u.tech_savviness_level IS NOT NULL AND u.d_sm_time IS NOT NULL
GROUP BY o.occupation_name, c.country_name, u.tech_savviness_level
HAVING COUNT(u.user_id) > 5
ORDER BY user_count DESC
LIMIT 30;

SELECT COUNT(*) FROM users;

SELECT ROUND(AVG(age), 1) FROM users;

SELECT primary_plat_id
FROM users
GROUP BY primary_plat_id
ORDER BY COUNT(*) DESC
LIMIT 1;

SELECT ROUND(AVG(monthly_income), 2) FROM users;

SELECT country_id
FROM users
GROUP BY country_id
ORDER BY COUNT(*) DESC
LIMIT 1;

SELECT device_sm_id
FROM users
GROUP BY device_sm_id
ORDER BY COUNT(*) DESC
LIMIT 1;

SELECT
    CASE
        WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
        WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    COUNT(u.user_id) AS total_users
FROM users u
WHERE u.primary_plat_id = %s
GROUP BY age_group
ORDER BY age_group;

SELECT
    g.gender,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN gender g ON u.gender_id = g.gender_id
WHERE u.primary_plat_id = %s
GROUP BY g.gender
ORDER BY total_users DESC;

SELECT
    c.country_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN countries c ON u.country_id = c.country_id
WHERE u.primary_plat_id = %s
GROUP BY c.country_name
ORDER BY total_users DESC
LIMIT 10;

SELECT
    o.occupation_name,
    COUNT(u.user_id) AS total_users
    FROM users u
    JOIN occupations o ON u.occupation_id = o.occupation_id
    WHERE u.primary_plat_id = %s
    GROUP BY o.occupation_name
    ORDER BY total_users DESC
    LIMIT 10;

SELECT
    CASE
        WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
        WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    COUNT(u.user_id) AS total_users
FROM users u
WHERE u.country_id = %s
GROUP BY age_group
ORDER BY age_group;

SELECT
    g.gender,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN gender g ON u.gender_id = g.gender_id
WHERE u.country_id = %s
GROUP BY g.gender
ORDER BY total_users DESC;

SELECT
    sm.socialm_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
WHERE u.country_id = %s
GROUP BY sm.socialm_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    e.entertainment_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
WHERE u.country_id = %s
GROUP BY e.entertainment_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
    ROUND(AVG(u.d_entertain_time), 2) AS avg_ent_time
FROM users u
WHERE u.country_id = %s;

SELECT
    ROUND(AVG(u.monthly_income), 2) AS avg_income,
    ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spent
FROM users u
WHERE u.country_id = %s;

SELECT
    CASE
        WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
        WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    COUNT(u.user_id) AS total_users
FROM users u
WHERE u.gender_id = %s
GROUP BY age_group
ORDER BY age_group;

SELECT
    sm.socialm_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
WHERE u.gender_id = %s
GROUP BY sm.socialm_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    e.entertainment_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
WHERE u.gender_id = %s
GROUP BY e.entertainment_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    o.occupation_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
WHERE u.gender_id = %s
GROUP BY o.occupation_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    ROUND(AVG(u.d_sm_time), 2) AS avg_sm_time,
    ROUND(AVG(u.d_entertain_time), 2) AS avg_ent_time
FROM users u
WHERE u.gender_id = %s;

SELECT
    ROUND(AVG(u.monthly_income), 2) AS avg_income,
    ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spent
FROM users u
WHERE u.gender_id = %s;

SELECT CASE
    WHEN u.age BETWEEN 0 AND 17 THEN '0-17' WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
    WHEN u.age BETWEEN 26 AND 35 THEN '26-35' WHEN u.age BETWEEN 36 AND 50 THEN '36-50' ELSE '51+'
    END AS age_group, COUNT(u.user_id) AS count
FROM users u WHERE u.preferred_content_id = %s GROUP BY age_group ORDER BY age_group;

SELECT g.gender, COUNT(u.user_id) AS count
FROM users u JOIN gender g ON u.gender_id = g.gender_id
WHERE u.preferred_content_id = %s GROUP BY g.gender ORDER BY count DESC;

SELECT
    c.country_name,
    COUNT(u.user_id) AS people
FROM users u
JOIN countries c ON u.country_id = c.country_id
WHERE u.preferred_content_id = %s
GROUP BY c.country_name
ORDER BY people DESC
LIMIT 5;

SELECT
    sm.socialm_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
WHERE u.preferred_content_id = %s
GROUP BY sm.socialm_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    o.occupation_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
WHERE u.preferred_content_id = %s
GROUP BY o.occupation_name
ORDER BY total_users DESC
LIMIT 5;

SELECT
    d.device_name,
    COUNT(u.user_id) AS total_users
FROM users u
JOIN devices d ON u.devide_for_entertainment_id = d.device_id
WHERE u.preferred_content_id = %s
GROUP BY d.device_name
ORDER BY total_users DESC;

SELECT
    CASE
        WHEN u.age BETWEEN 0 AND 17 THEN '0-17'
        WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN u.age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    g.gender,
    COUNT(u.user_id) AS count
FROM users u
JOIN gender g ON u.gender_id = g.gender_id
WHERE u.primary_plat_id = %s
GROUP BY age_group, g.gender
ORDER BY age_group, g.gender;

SELECT
    o.occupation_name,
    COUNT(u.user_id) AS user_count,
    ROUND(AVG(u.monthly_income), 2) AS avg_income
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
WHERE u.primary_plat_id = %s
GROUP BY o.occupation_name
ORDER BY user_count DESC
LIMIT 7;

SELECT
    e.entertainment_name,
    COUNT(u.user_id) AS user_count
FROM users u
JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
WHERE u.primary_plat_id = %s
GROUP BY e.entertainment_name
ORDER BY user_count DESC;

SELECT
    mg.goal_name,
    COUNT(u.user_id) AS user_count
FROM users u
JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
WHERE u.primary_plat_id = %s
GROUP BY mg.goal_name
ORDER BY user_count DESC;

SELECT
    CASE
        WHEN u.d_sm_time < 1 THEN 'Menos de 1h'
        WHEN u.d_sm_time BETWEEN 1 AND 2 THEN '1-2h'
        WHEN u.d_sm_time BETWEEN 2 AND 3 THEN '2-3h'
        WHEN u.d_sm_time BETWEEN 3 AND 4 THEN '3-4h'
        WHEN u.d_sm_time BETWEEN 4 AND 5 THEN '4-5h'
        ELSE 'Más de 5h'
    END AS time_bin,
    COUNT(u.user_id) AS user_count,
    ROUND(AVG(u.monthly_spent_entertain), 2) AS avg_spending
FROM users u
WHERE u.primary_plat_id = %s
GROUP BY time_bin
ORDER BY
    CASE time_bin
        WHEN 'Menos de 1h' THEN 1
        WHEN '1-2h' THEN 2
        WHEN '2-3h' THEN 3
        WHEN '3-4h' THEN 4
        WHEN '4-5h' THEN 5
        WHEN 'Más de 5h' THEN 6
        ELSE 7
    END;

SELECT d.device_name, COUNT(u.user_id) as count
FROM users u JOIN devices d ON u.device_sm_id = d.device_id
WHERE u.primary_plat_id = %s
GROUP BY d.device_name ORDER BY count DESC;

SELECT d.device_name, COUNT(u.user_id) as count
FROM users u JOIN devices d ON u.devide_for_entertainment_id = d.device_id
WHERE u.primary_plat_id = %s
GROUP BY d.device_name ORDER BY count DESC;

SELECT
    CASE
        WHEN monthly_income < 2000 THEN '< $2000'
        WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000 - $3999'
        WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000 - $5999'
        WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000 - $7999'
        ELSE '$8000+'
    END AS income_bracket,
    COUNT(user_id) AS user_count
FROM users
WHERE country_id = %s
GROUP BY income_bracket
ORDER BY
    CASE income_bracket
        WHEN '< $2000' THEN 1
        WHEN '$2000 - $3999' THEN 2
        WHEN '$4000 - $5999' THEN 3
        WHEN '$6000 - $7999' THEN 4
        WHEN '$8000+' THEN 5
        ELSE 6
    END;

SELECT
    CASE
        WHEN monthly_spent_entertain < 50 THEN '< $50'
        WHEN monthly_spent_entertain BETWEEN 50 AND 99 THEN '$50 - $99'
        WHEN monthly_spent_entertain BETWEEN 100 AND 149 THEN '$100 - $149'
        WHEN monthly_spent_entertain BETWEEN 150 AND 199 THEN '$150 - $199'
        ELSE '$200+'
    END AS spending_bracket,
    COUNT(user_id) AS user_count
FROM users
WHERE country_id = %s
GROUP BY spending_bracket
ORDER BY
    CASE spending_bracket
        WHEN '< $50' THEN 1
        WHEN '$50 - $99' THEN 2
        WHEN '$100 - $149' THEN 3
        WHEN '$150 - $199' THEN 4
        WHEN '$200+' THEN 5
        ELSE 6
    END;

SELECT
    o.occupation_name,
    COUNT(u.user_id) AS user_count
FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
WHERE u.country_id = %s
GROUP BY o.occupation_name
ORDER BY user_count DESC
LIMIT 10;

SELECT
    ROUND(AVG(avg_sleep_time), 1) AS avg_sleep,
    ROUND(AVG(physical_activity_tiem), 1) AS avg_activity,
    ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
    ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
FROM users
WHERE country_id = %s;

SELECT
    tech_savviness_level,
    COUNT(user_id) AS user_count
FROM users
WHERE country_id = %s
GROUP BY tech_savviness_level
ORDER BY tech_savviness_level;

SELECT sm.socialm_name, COUNT(u.user_id) as count
FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
WHERE u.gender_id = %s
GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;

SELECT sm.socialm_name, COUNT(u.user_id) as count
FROM users u JOIN social_media sm ON u.preferred_enter_plat_id = sm.socialm_id
WHERE u.gender_id = %s
GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;

SELECT
    CASE
        WHEN monthly_income < 2000 THEN '< $2000'
        WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000 - $3999'
        WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000 - $5999'
        WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000 - $7999'
        ELSE '$8000+'
    END AS income_bracket,
    COUNT(user_id) AS user_count,
    ROUND(AVG(monthly_spent_entertain), 2) AS avg_spending
FROM users
WHERE gender_id = %s
GROUP BY income_bracket
ORDER BY
    CASE income_bracket
        WHEN '< $2000' THEN 1 WHEN '$2000 - $3999' THEN 2 WHEN '$4000 - $5999' THEN 3
        WHEN '$6000 - $7999' THEN 4 WHEN '$8000+' THEN 5 ELSE 6
    END;

SELECT
    mg.goal_name,
    COUNT(u.user_id) AS user_count
FROM users u
JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
WHERE u.gender_id = %s
GROUP BY mg.goal_name
ORDER BY user_count DESC;

SELECT
    ROUND(AVG(ad_interaction_count), 1) AS avg_ad_interactions,
    ROUND(AVG(d_num_notifications), 0) AS avg_notifications,
    ROUND(AVG(tech_savviness_level), 1) AS avg_tech_savviness
FROM users
WHERE gender_id = %s;

SELECT CASE
    WHEN u.age BETWEEN 0 AND 17 THEN '0-17' WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
    WHEN u.age BETWEEN 26 AND 35 THEN '26-35' WHEN u.age BETWEEN 36 AND 50 THEN '36-50' ELSE '51+'
    END AS age_group, COUNT(u.user_id) AS count
FROM users u WHERE u.preferred_content_id = %s GROUP BY age_group ORDER BY age_group;

SELECT g.gender, COUNT(u.user_id) AS count
FROM users u JOIN gender g ON u.gender_id = g.gender_id
WHERE u.preferred_content_id = %s GROUP BY g.gender ORDER BY count DESC;

SELECT c.country_name, COUNT(u.user_id) AS count FROM users u
JOIN countries c ON u.country_id = c.country_id
WHERE u.preferred_content_id = %s GROUP BY c.country_name ORDER BY count DESC LIMIT 5;

SELECT o.occupation_name, COUNT(u.user_id) AS count FROM users u
JOIN occupations o ON u.occupation_id = o.occupation_id
WHERE u.preferred_content_id = %s GROUP BY o.occupation_name ORDER BY count DESC LIMIT 7;

SELECT CASE
    WHEN monthly_income < 2000 THEN '< $2000' WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2000-$3999'
    WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4000-$5999' WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6000-$7999'
    ELSE '$8000+'
    END AS income_bracket, COUNT(user_id) AS count
FROM users WHERE preferred_content_id = %s GROUP BY income_bracket ORDER BY MIN(monthly_income);

SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;

SELECT sm.socialm_name, COUNT(u.user_id) as count FROM users u
JOIN social_media sm ON u.preferred_enter_plat_id = sm.socialm_id
WHERE u.preferred_content_id = %s GROUP BY sm.socialm_name ORDER BY count DESC LIMIT 5;

SELECT d.device_name, COUNT(u.user_id) as count FROM users u
JOIN devices d ON u.devide_for_entertainment_id = d.device_id
WHERE u.preferred_content_id = %s GROUP BY d.device_name ORDER BY count DESC;

SELECT ROUND(AVG(d_entertain_time), 1) AS avg_ent, ROUND(AVG(d_sm_time), 1) AS avg_sm FROM users WHERE preferred_content_id = %s;

SELECT mg.goal_name, COUNT(u.user_id) AS count FROM users u JOIN media_goal mg ON u.primary_sm_goal_id = mg.goal_id
WHERE u.preferred_content_id = %s GROUP BY mg.goal_name ORDER BY count DESC;

SELECT ROUND(AVG(subscription_plats),1) AS avg_subs, ROUND(AVG(avg_sleep_time),1) AS avg_sleep,
               ROUND(AVG(physical_activity_tiem),1) AS avg_activity, ROUND(AVG(tech_savviness_level),1) AS avg_tech
FROM users WHERE preferred_content_id = %s;

SELECT COUNT(*) AS count FROM users;

SELECT ROUND(AVG(age), 1) AS avg_age FROM users;

SELECT ROUND(AVG(monthly_income), 2) AS avg_income FROM users;

SELECT sm.socialm_name, COUNT(u.user_id) AS user_count
FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
GROUP BY sm.socialm_name ORDER BY user_count DESC;

SELECT e.entertainment_name, COUNT(u.user_id) AS user_count
FROM users u JOIN entretaiment e ON u.preferred_content_id = e.entertainment_id
GROUP BY e.entertainment_name ORDER BY user_count DESC;

SELECT c.country_name, COUNT(u.user_id) AS user_count
FROM users u JOIN countries c ON u.country_id = c.country_id
GROUP BY c.country_name ORDER BY user_count DESC LIMIT 10;

SELECT sm.socialm_name, ROUND(AVG(u.monthly_income), 2) AS avg_income
FROM users u JOIN social_media sm ON u.primary_plat_id = sm.socialm_id
GROUP BY sm.socialm_name
HAVING COUNT(u.user_id) > 2
ORDER BY avg_income DESC LIMIT 1;

WITH RankedTech AS (
    SELECT primary_plat_id, AVG(tech_savviness_level) AS avg_tech
    FROM users GROUP BY primary_plat_id HAVING COUNT(user_id) > 2
)
SELECT sm.socialm_name, rt.avg_tech
FROM RankedTech rt JOIN social_media sm ON rt.primary_plat_id = sm.socialm_id
ORDER BY rt.avg_tech DESC LIMIT 1;

SELECT
    CASE
        WHEN monthly_income < 2000 THEN '< $2000' WHEN monthly_income BETWEEN 2000 AND 3999 THEN '$2k-$4k'
        WHEN monthly_income BETWEEN 4000 AND 5999 THEN '$4k-$6k' WHEN monthly_income BETWEEN 6000 AND 7999 THEN '$6k-$8k'
        ELSE '$8k+' END AS income_bracket,
    ROUND(AVG(subscription_plats), 1) AS avg_subs
FROM users GROUP BY income_bracket ORDER BY MIN(monthly_income);

SELECT AVG(d_num_notifications) FROM users;

SELECT
    CASE WHEN d_num_notifications > {threshold} THEN 'Notificaciones Altas (> {int(threshold)})' ELSE 'Notificaciones Bajas (<= {int(threshold)})' END AS notif_level,
    ROUND(AVG(avg_sleep_time), 1) AS avg_sleep
FROM users GROUP BY notif_level ORDER BY notif_level;

SELECT
    CASE WHEN d_gaming_time > {threshold} THEN 'Gamers (> {threshold}h)' ELSE 'No/Poco Gamers (<= {threshold}h)' END AS gaming_level,
    ROUND(AVG(d_sm_time), 1) AS avg_sm_time
FROM users GROUP BY gaming_level ORDER BY gaming_level;

SELECT
     CASE WHEN age <= 17 THEN '0-17' WHEN age <= 25 THEN '18-25' WHEN age <= 35 THEN '26-35'
           WHEN age <= 50 THEN '36-50' ELSE '51+' END AS age_group,
     ROUND(AVG(ad_interaction_count), 1) AS avg_interactions
FROM users GROUP BY age_group ORDER BY avg_interactions DESC LIMIT 1;

WITH OccPref AS (
    SELECT occupation_id, preferred_content_id, COUNT(user_id) AS group_count
    FROM users GROUP BY occupation_id, preferred_content_id
), TotalOcc AS (
    SELECT occupation_id, COUNT(user_id) AS total_in_occ FROM users GROUP BY occupation_id
), OverallPref AS (
    SELECT preferred_content_id, COUNT(user_id) * 1.0 / (SELECT COUNT(*) FROM users) AS overall_ratio
    FROM users GROUP BY preferred_content_id
)
SELECT o.occupation_name, e.entertainment_name,
       (op.group_count * 1.0 / toc.total_in_occ) / ovp.overall_ratio AS distinct_ratio
FROM OccPref op
JOIN TotalOcc toc ON op.occupation_id = toc.occupation_id
JOIN OverallPref ovp ON op.preferred_content_id = ovp.preferred_content_id
JOIN occupations o ON op.occupation_id = o.occupation_id
JOIN entretaiment e ON op.preferred_content_id = e.entertainment_id
WHERE ovp.overall_ratio > 0 AND toc.total_in_occ > 2
ORDER BY distinct_ratio DESC LIMIT 1;

SELECT c.country_name, ROUND(AVG(u.screen_time), 1) AS avg_screen_time
FROM users u JOIN countries c ON u.country_id = c.country_id
GROUP BY c.country_name HAVING COUNT(u.user_id) > 2
ORDER BY avg_screen_time DESC LIMIT 1;
