-- WARNING: THIS FILE IS FOR LOCAL USE ONLY.
-- DO NOT EXECUTE IT ON THE PRODUCTION SERVER.

CREATE DATABASE amnezia;
CREATE USER amnezia WITH ENCRYPTED PASSWORD 'I_AM_PRETTY_SURE_THIS_IS_FOR_LOCAL_USE_ONLY';
GRANT ALL PRIVILEGES ON DATABASE amnezia TO amnezia;