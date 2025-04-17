--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: habit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.habit (
    user_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    goal integer NOT NULL,
    frequency character varying(7) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    id uuid NOT NULL,
    CONSTRAINT check_frequency_valid CHECK (((frequency)::text = ANY ((ARRAY['daily'::character varying, 'weekly'::character varying, 'monthly'::character varying])::text[])))
);


ALTER TABLE public.habit OWNER TO postgres;

--
-- Name: progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.progress (
    user_id uuid NOT NULL,
    habit_id uuid NOT NULL,
    current integer NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    created_date date DEFAULT now() NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.progress OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    telegram_chat_id integer NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
0a7fe2652273
\.


--
-- Data for Name: habit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.habit (user_id, title, goal, frequency, created_at, id) FROM stdin;
cf9333d7-e7f7-4c47-8f8b-0d4400371d2a	push ups	100	daily	2025-04-17 03:24:31.546468	dc259890-58cc-4625-901a-ccb620090fc4
a8acb288-6649-4bc1-b390-8c98879558ec	push ups	100	daily	2025-04-17 03:24:31.552753	630d584b-f8fb-458a-97d1-a66831611841
a8acb288-6649-4bc1-b390-8c98879558ec	reading	1	daily	2025-04-17 03:24:31.555872	8f0ba12b-79bd-470f-aefe-26a77a7b20d5
\.


--
-- Data for Name: progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.progress (user_id, habit_id, current, updated_at, created_date, id) FROM stdin;
-- User: cf9333d7-e7f7-4c47-8f8b-0d4400371d2a | Habit: dc259890-58cc-4625-901a-ccb620090fc4 (push ups)
cf9333d7-e7f7-4c47-8f8b-0d4400371d2a	dc259890-58cc-4625-901a-ccb620090fc4	20	2025-04-15 06:00:00	2025-04-15	ab91dfe5-1a6f-4d96-b8a3-fd3e1f749c95
cf9333d7-e7f7-4c47-8f8b-0d4400371d2a	dc259890-58cc-4625-901a-ccb620090fc4	25	2025-04-16 06:00:00	2025-04-16	d899e87d-6db5-4d0e-892c-d0c9c7c6a742
cf9333d7-e7f7-4c47-8f8b-0d4400371d2a	dc259890-58cc-4625-901a-ccb620090fc4	30	2025-04-17 06:00:00	2025-04-17	113aa395-c9e5-405e-b6c4-7e77ed5bbf5f

-- User: a8acb288-6649-4bc1-b390-8c98879558ec | Habit 1: 630d584b-f8fb-458a-97d1-a66831611841 (push ups)
a8acb288-6649-4bc1-b390-8c98879558ec	630d584b-f8fb-458a-97d1-a66831611841	15	2025-04-15 07:10:00	2025-04-15	e0cb4f6e-1ef6-4c6f-8f6c-8e4b33a989f4
a8acb288-6649-4bc1-b390-8c98879558ec	630d584b-f8fb-458a-97d1-a66831611841	20	2025-04-16 07:10:00	2025-04-16	6eaa8b7a-4720-4e80-a660-bebfb76ed2d3
a8acb288-6649-4bc1-b390-8c98879558ec	630d584b-f8fb-458a-97d1-a66831611841	25	2025-04-17 07:10:00	2025-04-17	c0f69ee5-f95e-4393-865e-d9ea9ab64643

-- User: a8acb288-6649-4bc1-b390-8c98879558ec | Habit 2: 8f0ba12b-79bd-470f-aefe-26a77a7b20d5 (reading)
a8acb288-6649-4bc1-b390-8c98879558ec	8f0ba12b-79bd-470f-aefe-26a77a7b20d5	1	2025-04-15 08:00:00	2025-04-15	7e059af6-eabb-4428-a74e-512ecfd63265
a8acb288-6649-4bc1-b390-8c98879558ec	8f0ba12b-79bd-470f-aefe-26a77a7b20d5	1	2025-04-16 08:00:00	2025-04-16	9e6a8e7a-bb61-4e45-a124-0cd17ebea3cd
a8acb288-6649-4bc1-b390-8c98879558ec	8f0ba12b-79bd-470f-aefe-26a77a7b20d5	1	2025-04-17 08:00:00	2025-04-17	3cd6a4e9-7a65-4416-aef4-5c362b88d8b1
\.

--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (telegram_chat_id, id) FROM stdin;
123	8cf50ebd-776c-4fb2-9ea6-1719c08ac604
321	cf9333d7-e7f7-4c47-8f8b-0d4400371d2a
567	a8acb288-6649-4bc1-b390-8c98879558ec
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: habit habit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habit
    ADD CONSTRAINT habit_pkey PRIMARY KEY (id);


--
-- Name: progress progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_pkey PRIMARY KEY (id);


--
-- Name: habit uq_user_title; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habit
    ADD CONSTRAINT uq_user_title UNIQUE (user_id, title);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_telegram_chat_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_telegram_chat_id_key UNIQUE (telegram_chat_id);


--
-- Name: habit habit_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habit
    ADD CONSTRAINT habit_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: progress progress_habit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_habit_id_fkey FOREIGN KEY (habit_id) REFERENCES public.habit(id);


--
-- Name: progress progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

