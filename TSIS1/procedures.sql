--1. Insert or Update (Upsert) Procedure
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
AS $$
BEGIN
    INSERT INTO phonebook (first_name, phone_number)
    VALUES (p_name, p_phone)
    ON CONFLICT (first_name) 
    DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$ LANGUAGE plpgsql;

--2. Bulk Insert with Validation
CREATE OR REPLACE FUNCTION bulk_insert_with_validation(names TEXT[], phones TEXT[])
RETURNS TABLE(invalid_name TEXT, invalid_phone TEXT) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(names, 1) LOOP
        -- Simple validation: phone must be digits and length 11
        IF phones[i] ~ '^[0-9]{11}$' THEN
            INSERT INTO phonebook (first_name, phone_number)
            VALUES (names[i], phones[i])
            ON CONFLICT DO NOTHING;
        ELSE
            invalid_name := names[i];
            invalid_phone := phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

--3. Delete Procedure
CREATE OR REPLACE PROCEDURE delete_contact_by_data(p_identifier TEXT)
AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE first_name = p_identifier 
       OR phone_number = p_identifier;
END;
$$ LANGUAGE plpgsql;

--4. Add a phone number
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, 
    p_phone VARCHAR, 
    p_type VARCHAR
)
AS $$
BEGIN
    -- We check if the contact exists first
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_contact_name) THEN
        UPDATE phonebook 
        SET phone_number = p_phone,
            phone_type = p_type
        WHERE first_name = p_contact_name;
    ELSE
        -- Optional: If contact doesn't exist, you can raise an error 
        -- or choose to insert them instead.
        RAISE NOTICE 'Contact % not found. No phone added.', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

--5. Move to group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, 
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- 1. Try to find the group first
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- 2. Only insert if it really isn't there
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) 
        VALUES (p_group_name) 
        RETURNING id INTO v_group_id;
    END IF;

    -- 3. Update the contact
    UPDATE phonebook 
    SET group_id = v_group_id
    WHERE first_name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact % not found.', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;