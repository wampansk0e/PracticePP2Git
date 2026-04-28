-- Удаляем старые версии функций, чтобы изменить структуру колонок
DROP FUNCTION IF EXISTS get_contacts_by_pattern(TEXT);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

-- 1. Pattern Matching Function
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, email VARCHAR, group_id VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        p.id, 
        p.first_name, 
        p.email, 
        p.group_id::VARCHAR -- Keep the cast we added earlier
    FROM phonebook p
    WHERE p.first_name ILIKE '%' || search_pattern || '%' 
       OR p.phone_number LIKE '%' || search_pattern || '%'
       OR p.email ILIKE '%' || search_pattern || '%'; -- NEW: Email partial match
END;
$$ LANGUAGE plpgsql;

-- 2. Pagination Function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id, p.first_name, p.phone_number 
    FROM phonebook p
    ORDER BY p.id  -- Исправлено с contact_id на id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

--3. Filter by group — show only contacts belonging to a selected category.
CREATE OR REPLACE FUNCTION get_contacts_by_group(p_group_id INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone_number VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id, p.first_name, p.phone_number, p.email
    FROM phonebook p
    WHERE p.group_id = p_group_id
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;
