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