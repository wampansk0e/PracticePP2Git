-- 1.Pattern Matching Function
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    WHERE first_name ILIKE '%' || search_pattern || '%' 
       OR phone_number LIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;

--2.Pagination Function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    ORDER BY contact_id 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;