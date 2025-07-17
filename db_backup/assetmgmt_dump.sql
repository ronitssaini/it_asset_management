--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ronitsaini
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ronitsaini;

--
-- Name: assets; Type: TABLE; Schema: public; Owner: ronitsaini
--

CREATE TABLE public.assets (
    serial_number character varying(50) NOT NULL,
    company_name character varying(100) NOT NULL,
    device_type character varying(50) NOT NULL,
    make character varying(50),
    os_version character varying(50),
    ip_address character varying(50),
    subnet_mask character varying(50),
    purchase_date date,
    additional_device character varying(100),
    remarks text,
    location character varying(100),
    typer character varying(50),
    processor_type character varying(50),
    processor character varying(50),
    total_processor_core integer,
    internal_hard_disk character varying(50),
    disk_type character varying(50),
    qty integer,
    raid character varying(10),
    ram character varying(20),
    network_card character varying(100),
    hba_card character varying(100),
    model character varying(100),
    no_of_ports integer,
    hard_disk character varying(50),
    monitor character varying(100),
    employee_code character varying(50),
    employee_name character varying(100),
    function character varying(100),
    role character varying(100),
    total_capacity character varying(50),
    last_users text
);


ALTER TABLE public.assets OWNER TO ronitsaini;

--
-- Name: users; Type: TABLE; Schema: public; Owner: ronitsaini
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50),
    email character varying(100),
    hashed_password character varying(255),
    is_active boolean,
    role character varying(20)
);


ALTER TABLE public.users OWNER TO ronitsaini;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: ronitsaini
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO ronitsaini;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ronitsaini
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: ronitsaini
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ronitsaini
--

COPY public.alembic_version (version_num) FROM stdin;
a21fa5c11e29
\.


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: ronitsaini
--

COPY public.assets (serial_number, company_name, device_type, make, os_version, ip_address, subnet_mask, purchase_date, additional_device, remarks, location, typer, processor_type, processor, total_processor_core, internal_hard_disk, disk_type, qty, raid, ram, network_card, hba_card, model, no_of_ports, hard_disk, monitor, employee_code, employee_name, function, role, total_capacity, last_users) FROM stdin;
PGT9877	SAPL	Desktop	LENOVO	Windows 10	172.17.02	255.255.255.0	\N	Wireless Mouse	NaN	Mohali	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	500 GB	19" LED	2800153	Chint Ram	Finance	NaN	\N	["Ronit", "Chint Ram"]
SWITCH0003	VTL	Switch	CISCO	IOS 10.1	177.17.1.3	255.255.0.0	2020-07-23	\N	\N	Mohali	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
STR0001	VTL	Storage	\N	\N	\N	\N	\N	\N	\N	Delhi	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD01-P	SAPL	Server	DELL	Windows	10.1.1.1	255.255.255.0	\N	\N	\N	GND floor	Physical	\N	2	\N	\N	\N	3	1	96GB	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD01-V	SAPL	Server	DELL	Windows	10.1.1.1	255.255.255.0	\N	\N	\N	GND floor	Virtual	\N	2	\N	\N	\N	3	1	96GB	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD01-V1	STPL	Server	\N	\N	\N	\N	\N	\N	\N	GND floor	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
ASDFGH	SAPL	Switch	CISCO	IOS 10.1	172.17.1.1	255.255.0.0	\N	\N	\N	Mohali	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD01-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD02-P	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD02-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD03-P	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD03-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD04-P	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD04-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD05-P	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD05-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD06-P	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
POKLD06-V2	SAPL	Server	DELL	Windows	\N	255.255.255.0	\N	\N	\N	GND floor	\N	\N	2	\N	460GB	SSD	3	1	\N	2- 10G	2- 32GB	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
STOR0001	SAPL	Storage	Synology	DSM 7.1	192.168.0.10	255.255.255.0	2022-01-10	NaN	Backup storage unit	\N	\N	\N	\N	\N	\N	HDD	\N	\N	\N	\N	\N	DS220+	\N	\N	\N	\N	\N	\N	\N	8TB	\N
STOR0002	VTL	Storage	DELL	Windows 10	192.168.0.11	255.255.255.0	2023-03-15	UPS Backup	High-performance use	\N	\N	\N	\N	\N	\N	SSD	\N	\N	\N	\N	\N	PowerVault	\N	\N	\N	\N	\N	\N	\N	12TB	\N
STOR0003	SAPL	Storage	Buffalo	NAS OS	192.168.0.12	255.255.255.0	2021-11-25	External Drive	Used for archiving	\N	\N	\N	\N	\N	\N	HDD	\N	\N	\N	\N	\N	TeraStation	\N	\N	\N	\N	\N	\N	\N	16TB	\N
STOR0004	VTL	Storage	WD	My Cloud	192.168.0.13	255.255.255.0	2020-07-30	NaN	Finance backups	\N	\N	\N	\N	\N	\N	SSD	\N	\N	\N	\N	\N	EX4100	\N	\N	\N	\N	\N	\N	\N	8TB	\N
STOR0005	SAPL	Storage	Pure	Purity	192.168.0.14	255.255.255.0	2023-06-10	UPS	Core DB backup	\N	\N	\N	\N	\N	\N	SSD	\N	\N	\N	\N	\N	FlashArray	\N	\N	\N	\N	\N	\N	\N	24TB	\N
STOR0006	VTL	Storage	EMC	Unisphere	192.168.0.15	255.255.255.0	2022-09-05	External NAS	Project drive	\N	\N	\N	\N	\N	\N	SSD	\N	\N	\N	\N	\N	Unity XT	\N	\N	\N	\N	\N	\N	\N	20TB	\N
STOR0007	SAPL	Storage	Zyxel	Linux	192.168.0.16	255.255.255.0	2021-02-14	NaN	Light storage use	\N	\N	\N	\N	\N	\N	HDD	\N	\N	\N	\N	\N	NAS326	\N	\N	\N	\N	\N	\N	\N	4TB	\N
STOR0008	VTL	Storage	QNAP	QTS	192.168.0.17	255.255.255.0	2022-12-21	RAID Controller	Encrypted backup NAS	\N	\N	\N	\N	\N	\N	SSD	\N	\N	\N	\N	\N	TS-453D	\N	\N	\N	\N	\N	\N	\N	10TB	\N
PG005QZK	SAPL	Desktop	LENOVO	Windows 10	172.17.01	255.255.255.0	\N	Wireless Mouse	NaN	Mohali	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	500 GB	19" LED	2100357	Keshav Suleria	Finance	NaN	\N	["Ronit"]
PGT9846	SAPL	Desktop	LENOVO	Windows 10	172.17.04	255.255.255.0	\N	Wireless Mouse	NaN	Mohali	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	160 GB	19" LED	1701044	Gurdeep Singh	Finance	NaN	\N	["Gurdeep Singh"]
PG0130PY	SAPL	Desktop	LENOVO	Windows 10	172.17.03	255.255.255.0	\N	Wireless Mouse	NaN	Mohali	\N	\N	Intel(R) Core(TM) i3-6100 CPU @3.60GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	500 GB	19" LED	2800176	Ram Kumar	Finance	NaN	\N	["AArush", "Ronit", "User 1"]
PG011CPN	SAPL	Desktop	LENOVO	Windows 10	172.17.05	255.255.255.0	\N	Wireless Mouse	NaN	Mohali	\N	\N	Intel(R) Core(TM) i3-6100 CPU @3.60GHz	\N	\N	\N	\N	\N	8 GB	\N	\N	\N	\N	1 TB	19" LED	1750158	Abhishek Kumar	CORE NETWORK	NaN	\N	["Abhishek Kumar"]
PG4694A	SAPL	Laptop	HP	Windows 11	172.17.40	255.255.255.0	\N	Wireless Mouse	\N	Gurugram	\N	\N	Intel(R) Core(TM) i7-10510U @1.80GHz	\N	\N	\N	\N	\N	8 GB	\N	\N	\N	\N	512 GB	19" LED	2100357	Keshav Suleria	IT	\N	\N	["Keshav Suleria"]
PG5224B	SAPL	Laptop	HP	Windows 11	172.17.1	255.255.255.0	\N	Wireless Mouse	\N	Delhi	\N	\N	AMD Ryzen 5 3500U	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	256 GB	19" LED	2100358	Chint Ram	IT	\N	\N	["Chint Ram"]
PG5888C	SAPL	Desktop	HP	Windows 11	172.17.44	255.255.255.0	\N	Wireless Mouse	\N	Gurugram	\N	\N	Intel(R) Core(TM) i3-6100 CPU @3.60GHz	\N	\N	\N	\N	\N	16 GB	\N	\N	\N	\N	512 GB	19" LED	2100359	Ram Kumar	IT	\N	\N	["Ram Kumar"]
PG9689D	SAPL	Desktop	Asus	Windows 11	172.17.21	255.255.255.0	\N	Wireless Mouse	\N	Noida	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	512 GB	15.6" LED	2100360	Anita Sharma	Finance	\N	\N	["Anita Sharma"]
PG4885E	SAPL	Desktop	Asus	Windows 10	172.17.17	255.255.255.0	\N	Wireless Mouse	\N	Delhi	\N	\N	Intel(R) Core(TM) i5-8250U @1.60GHz	\N	\N	\N	\N	\N	16 GB	\N	\N	\N	\N	256 GB	19" LED	2100361	Vikram Singh	Operations	\N	\N	["Vikram Singh"]
PG1279F	SAPL	Desktop	Acer	Windows 11	172.17.34	255.255.255.0	\N	Wireless Mouse	\N	Gurugram	\N	\N	AMD Ryzen 5 3500U	\N	\N	\N	\N	\N	16 GB	\N	\N	\N	\N	256 GB	19" LED	2100362	Divya Patel	Admin	\N	\N	["Divya Patel"]
PG1358G	SAPL	Desktop	Asus	Windows 11	172.17.23	255.255.255.0	\N	Wireless Mouse	\N	Delhi	\N	\N	AMD Ryzen 5 3500U	\N	\N	\N	\N	\N	8 GB	\N	\N	\N	\N	1024 GB	15.6" LED	2100363	Nitin Verma	Operations	\N	\N	["Nitin Verma"]
PG4953H	SAPL	Laptop	Dell	Windows 11	172.17.29	255.255.255.0	\N	Wireless Mouse	\N	Noida	\N	\N	Intel(R) Core(TM) i5-8250U @1.60GHz	\N	\N	\N	\N	\N	8 GB	\N	\N	\N	\N	500 GB	15.6" LED	2100364	Sunita Joshi	Operations	\N	\N	["Sunita Joshi"]
PG6014I	SAPL	Desktop	Acer	Windows 10	172.17.34	255.255.255.0	\N	Wireless Mouse	\N	Mohali	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	8 GB	\N	\N	\N	\N	512 GB	14" LED	2100365	Ramesh Chauhan	Admin	\N	\N	["Ramesh Chauhan"]
PG5597J	SAPL	Desktop	HP	Windows 10	172.17.2	255.255.255.0	\N	Wireless Mouse	\N	Gurugram	\N	\N	Intel(R) Core(TM) i5-8250U @1.60GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	512 GB	15.6" LED	2100366	Preeti Mehra	IT	\N	\N	["Preeti Mehra"]
PG5294K	SAPL	Desktop	Acer	Windows 11	172.17.19	255.255.255.0	\N	Wireless Mouse	\N	Delhi	\N	\N	Intel(R) Core(TM) i7-10510U @1.80GHz	\N	\N	\N	\N	\N	16 GB	\N	\N	\N	\N	256 GB	14" LED	2100367	Aditya Kapoor	Operations	\N	\N	["Aditya Kapoor"]
PG8568L	SAPL	Laptop	HP	Windows 11	172.17.12	255.255.255.0	\N	Wireless Mouse	\N	Noida	\N	\N	Intel(R) Core(TM) i7-10510U @1.80GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	512 GB	15.6" LED	2100368	Neelam Rathi	Admin	\N	\N	["Neelam Rathi"]
PG6700M	SAPL	Laptop	Acer	Windows 10	172.17.14	255.255.255.0	\N	Wireless Mouse	\N	Mohali	\N	\N	Intel(R) Core(TM) i3-3220 CPU @3.30GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	256 GB	15.6" LED	2100369	Yashwant Rao	Admin	\N	\N	["Yashwant Rao"]
PG8825N	SAPL	Desktop	Asus	Windows 10	172.17.3	255.255.255.0	\N	Wireless Mouse	\N	Noida	\N	\N	Intel(R) Core(TM) i7-10510U @1.80GHz	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	1024 GB	14" LED	2100370	Pooja Thakur	Admin	\N	\N	["Pooja Thakur"]
PG5418O	SAPL	Laptop	Dell	Windows 10	172.17.11	255.255.255.0	\N	Wireless Mouse	\N	Delhi	\N	\N	AMD Ryzen 5 3500U	\N	\N	\N	\N	\N	4 GB	\N	\N	\N	\N	512 GB	15.6" LED	2100371	Mohit Bansal	IT	\N	\N	["Mohit Bansal"]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ronitsaini
--

COPY public.users (id, username, email, hashed_password, is_active, role) FROM stdin;
1	admin	admin@example.com	$2b$12$x5BgdOB5QNELO3b2aLMuYuUmd0CD4S6eOnPo058QzvqQyoN3w6GD6	t	admin
3	admin 2	admin69@gmail.com	$2b$12$pNiICIMRC/5EOXyIFi658O6XeyiYP/sWUw8pAoT/Aa0qtbXDn/B3.	t	admin
4	Ronit Saini	the.wron1t@gmail.com	$2b$12$mS8PHZdee56cO.K9gE99G.aszJwgLI7l8rJMUL1c994RdQZWaC3de	t	manager
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ronitsaini
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ronitsaini
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: assets assets_pkey; Type: CONSTRAINT; Schema: public; Owner: ronitsaini
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (serial_number);


--
-- Name: assets assets_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: ronitsaini
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_serial_number_key UNIQUE (serial_number);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ronitsaini
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: ronitsaini
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: ronitsaini
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: ronitsaini
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- PostgreSQL database dump complete
--

