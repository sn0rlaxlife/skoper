-- Create table to store recommendations
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    recommendation_text TEXT
);

-- Insert CIS Benchmark recommendations
INSERT INTO recommendations (recommendation_text)
VALUES
    ('Enable automatic security updates on all virtual machines.'),
    ('Implement multi-factor authentication (MFA) for all user accounts.'),
    ('Regularly review and update network security group rules.'),
    ('Ensure that all virtual machines are running on supported operating systems.'),
    ('Apply security patches to virtual machines within 30 days of release.'),
    ('Disable default administrative accounts and create unique accounts for each user.');

-- Query to retrieve all recommendations
SELECT * FROM recommendations;

-- Query to retrieve recommendations matching a specific criterion (example: CIS Benchmark recommendations)
SELECT * FROM recommendations
WHERE recommendation_text LIKE '%CIS Benchmark%';
