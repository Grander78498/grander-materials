--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

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
-- Name: album; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.album (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    release_date date NOT NULL,
    release_type_id smallint NOT NULL,
    duration interval
);


ALTER TABLE public.album OWNER TO postgres;

--
-- Name: album_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.album_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.album_id_seq OWNER TO postgres;

--
-- Name: album_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.album_id_seq OWNED BY public.album.id;


--
-- Name: album_performer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.album_performer (
    album_id bigint NOT NULL,
    performer_id bigint NOT NULL
);


ALTER TABLE public.album_performer OWNER TO postgres;

--
-- Name: group_musician; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_musician (
    group_id bigint NOT NULL,
    musician_id bigint NOT NULL
);


ALTER TABLE public.group_musician OWNER TO postgres;

--
-- Name: music_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.music_group (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    country character varying(100) NOT NULL,
    creation_date date
);


ALTER TABLE public.music_group OWNER TO postgres;

--
-- Name: music_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.music_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.music_group_id_seq OWNER TO postgres;

--
-- Name: music_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.music_group_id_seq OWNED BY public.music_group.id;


--
-- Name: musician; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.musician (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    country character varying(100) NOT NULL,
    birth_date date
);


ALTER TABLE public.musician OWNER TO postgres;

--
-- Name: musician_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.musician_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.musician_id_seq OWNER TO postgres;

--
-- Name: musician_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.musician_id_seq OWNED BY public.musician.id;


--
-- Name: performer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.performer (
    id bigint NOT NULL,
    musician_id bigint,
    group_id bigint
);


ALTER TABLE public.performer OWNER TO postgres;

--
-- Name: performer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.performer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.performer_id_seq OWNER TO postgres;

--
-- Name: performer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.performer_id_seq OWNED BY public.performer.id;


--
-- Name: producer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producer (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    country character varying(100) NOT NULL,
    birth_date date
);


ALTER TABLE public.producer OWNER TO postgres;

--
-- Name: producer_album; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producer_album (
    producer_id bigint NOT NULL,
    album_id bigint NOT NULL
);


ALTER TABLE public.producer_album OWNER TO postgres;

--
-- Name: producer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.producer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.producer_id_seq OWNER TO postgres;

--
-- Name: producer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.producer_id_seq OWNED BY public.producer.id;


--
-- Name: producer_song; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producer_song (
    producer_id bigint NOT NULL,
    song_id bigint NOT NULL
);


ALTER TABLE public.producer_song OWNER TO postgres;

--
-- Name: release_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_type (
    id smallint NOT NULL,
    type character varying(30)
);


ALTER TABLE public.release_type OWNER TO postgres;

--
-- Name: release_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_type_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_type_id_seq OWNER TO postgres;

--
-- Name: release_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_type_id_seq OWNED BY public.release_type.id;


--
-- Name: single; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.single (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    release_date date NOT NULL
);


ALTER TABLE public.single OWNER TO postgres;

--
-- Name: single_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.single_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.single_id_seq OWNER TO postgres;

--
-- Name: single_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.single_id_seq OWNED BY public.single.id;


--
-- Name: single_song; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.single_song (
    single_id bigint NOT NULL,
    song_id bigint NOT NULL
);


ALTER TABLE public.single_song OWNER TO postgres;

--
-- Name: song; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.song (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    duration interval NOT NULL,
    album_id bigint
);


ALTER TABLE public.song OWNER TO postgres;

--
-- Name: song_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.song_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.song_id_seq OWNER TO postgres;

--
-- Name: song_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.song_id_seq OWNED BY public.song.id;


--
-- Name: song_performer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.song_performer (
    song_id bigint NOT NULL,
    performer_id bigint NOT NULL
);


ALTER TABLE public.song_performer OWNER TO postgres;

--
-- Name: album id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album ALTER COLUMN id SET DEFAULT nextval('public.album_id_seq'::regclass);


--
-- Name: music_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_group ALTER COLUMN id SET DEFAULT nextval('public.music_group_id_seq'::regclass);


--
-- Name: musician id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musician ALTER COLUMN id SET DEFAULT nextval('public.musician_id_seq'::regclass);


--
-- Name: performer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performer ALTER COLUMN id SET DEFAULT nextval('public.performer_id_seq'::regclass);


--
-- Name: producer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer ALTER COLUMN id SET DEFAULT nextval('public.producer_id_seq'::regclass);


--
-- Name: release_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_type ALTER COLUMN id SET DEFAULT nextval('public.release_type_id_seq'::regclass);


--
-- Name: single id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single ALTER COLUMN id SET DEFAULT nextval('public.single_id_seq'::regclass);


--
-- Name: song id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song ALTER COLUMN id SET DEFAULT nextval('public.song_id_seq'::regclass);


--
-- Data for Name: album; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.album (id, name, release_date, release_type_id, duration) FROM stdin;
1	...Like Clockwork	2013-06-03	1	\N
2	Songs For The Deaf	2002-08-27	1	\N
3	Welcome To Sky Valley	1994-06-28	1	\N
4	Wish You Were Here	1975-09-12	1	\N
5	OK Computer	1997-05-21	1	\N
6	Watch The Throne	2011-08-08	1	\N
7	Kids See Ghosts	2018-06-08	2	\N
8	My Beautiful Dark Twisted Fantasy	2010-11-22	1	\N
9	PULSE	1995-05-28	3	00:06:35
\.


--
-- Data for Name: album_performer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.album_performer (album_id, performer_id) FROM stdin;
1	1
2	1
3	2
4	3
5	4
6	6
6	7
7	5
7	6
7	11
8	6
9	3
\.


--
-- Data for Name: group_musician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_musician (group_id, musician_id) FROM stdin;
1	1
1	2
1	3
1	4
2	1
2	3
2	5
2	6
3	7
3	8
4	9
4	10
5	11
5	16
\.


--
-- Data for Name: music_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.music_group (id, name, country, creation_date) FROM stdin;
1	Queens Of The Stone Age	USA	1996-01-01
2	Kyuss	USA	1987-01-01
3	Pink Floyd	Great Britain	1965-01-01
4	Radiohead	Great Britain	1985-01-01
5	Kids See Ghosts	USA	2018-01-01
\.


--
-- Data for Name: musician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.musician (id, name, country, birth_date) FROM stdin;
1	Josh Homme	USA	1973-05-17
2	Dave Grohl	USA	1969-01-14
3	Nick Oliveri	USA	1971-10-21
4	Mark Lanegan	USA	1964-11-25
5	Brant Bjork	USA	1973-03-19
6	John Garcia	USA	1970-09-04
7	David Gilmour	Great Britain	1946-03-06
8	Roger Waters	Great Britain	1943-09-06
9	Thom Yorke	Great Britain	1968-10-07
10	Colin Greenwood	Great Britain	1969-06-26
11	Kanye West	USA	1977-06-08
12	JAY-Z	USA	1969-12-04
13	Frank Ocean	USA	1987-10-28
14	The-Dream	USA	1977-09-20
15	Pusha T	USA	1977-05-13
16	Kid Cudi	USA	1984-01-30
17	Raekwon	USA	1970-01-12
\.


--
-- Data for Name: performer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.performer (id, musician_id, group_id) FROM stdin;
1	\N	1
2	\N	2
3	\N	3
4	\N	4
5	\N	5
6	11	\N
7	12	\N
8	13	\N
9	14	\N
10	15	\N
11	16	\N
12	17	\N
\.


--
-- Data for Name: producer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producer (id, name, country, birth_date) FROM stdin;
1	Josh Homme	USA	1973-05-17
2	Eric Valentine	USA	1968-03-07
3	Adam Kasper	USA	1962-12-01
4	Chris Goss	USA	1959-08-17
5	Roger Waters	Great Britain	1943-09-06
6	David Gilmour	Great Britain	1946-03-06
7	Nigel Godrich	Great Britain	1971-02-28
8	Kanye West	USA	1977-06-08
9	Kid Cudi	USA	1984-01-30
10	Mike Dean	USA	1965-03-01
\.


--
-- Data for Name: producer_album; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producer_album (producer_id, album_id) FROM stdin;
1	1
1	2
2	2
3	2
4	3
5	4
6	4
7	5
8	6
10	6
8	7
9	7
10	7
8	8
10	8
6	9
\.


--
-- Data for Name: producer_song; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producer_song (producer_id, song_id) FROM stdin;
7	14
\.


--
-- Data for Name: release_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.release_type (id, type) FROM stdin;
1	LP
2	EP
3	Live
4	Compilation
\.


--
-- Data for Name: single; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.single (id, name, release_date) FROM stdin;
1	My God Is The Sun	2013-04-08
2	No One Knows	2002-11-26
3	Gardenia	1995-01-01
4	Have A Cigar	1975-11-15
5	Paranoid Android	1997-05-26
6	No Church In The Wild	2012-03-20
7	N****s In Paris	2011-09-13
8	POWER	2010-07-01
9	Runaway	2010-10-04
\.


--
-- Data for Name: single_song; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.single_song (single_id, song_id) FROM stdin;
1	1
2	3
3	5
4	9
4	8
5	12
5	13
5	14
6	15
7	16
8	18
9	19
\.


--
-- Data for Name: song; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.song (id, name, duration, album_id) FROM stdin;
1	I Sat By The Ocean	00:03:55	1
2	My God Is The Sun	00:03:55	1
3	No One Knows	00:04:38	2
4	A Song For The Dead	00:05:52	2
5	Gardenia	00:06:54	3
6	Space Cadet	00:07:02	3
7	Shine on You Crazy Diamond (Parts I-V)	00:13:30	4
8	Welcome To The Machine	00:07:31	4
9	Have A Cigar	00:05:08	4
10	Wish You Were Here	00:05:40	4
11	Shine on You Crazy Diamond (Parts VI-IX)	00:12:31	4
12	Paranoid Android	00:06:23	5
13	Let Down	00:04:59	5
14	Pearly	00:03:33	\N
15	No Church In The Wild	00:04:32	6
16	N****s In Paris	00:03:39	6
17	Gorgeous	00:05:57	8
18	POWER	00:04:52	8
19	Runaway	00:09:07	8
20	Feel The Love	00:02:33	7
21	Cudi Montage	00:03:17	7
22	Wish You Were Here - Live	00:06:35	9
\.


--
-- Data for Name: song_performer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.song_performer (song_id, performer_id) FROM stdin;
14	4
15	8
15	9
17	11
17	12
19	10
20	10
\.


--
-- Name: album_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.album_id_seq', 9, true);


--
-- Name: music_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.music_group_id_seq', 5, true);


--
-- Name: musician_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.musician_id_seq', 17, true);


--
-- Name: performer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.performer_id_seq', 12, true);


--
-- Name: producer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.producer_id_seq', 10, true);


--
-- Name: release_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.release_type_id_seq', 4, true);


--
-- Name: single_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.single_id_seq', 9, true);


--
-- Name: song_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.song_id_seq', 22, true);


--
-- Name: album_performer album_performer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album_performer
    ADD CONSTRAINT album_performer_pkey PRIMARY KEY (album_id, performer_id);


--
-- Name: album album_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: group_musician group_musician_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_musician
    ADD CONSTRAINT group_musician_pkey PRIMARY KEY (group_id, musician_id);


--
-- Name: music_group music_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_group
    ADD CONSTRAINT music_group_name_key UNIQUE (name);


--
-- Name: music_group music_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_group
    ADD CONSTRAINT music_group_pkey PRIMARY KEY (id);


--
-- Name: musician musician_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musician
    ADD CONSTRAINT musician_pkey PRIMARY KEY (id);


--
-- Name: performer performer_musician_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performer
    ADD CONSTRAINT performer_musician_id_group_id_key UNIQUE (musician_id, group_id);


--
-- Name: performer performer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performer
    ADD CONSTRAINT performer_pkey PRIMARY KEY (id);


--
-- Name: producer_album producer_album_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_album
    ADD CONSTRAINT producer_album_pkey PRIMARY KEY (producer_id, album_id);


--
-- Name: producer producer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer
    ADD CONSTRAINT producer_pkey PRIMARY KEY (id);


--
-- Name: producer_song producer_song_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_song
    ADD CONSTRAINT producer_song_pkey PRIMARY KEY (producer_id, song_id);


--
-- Name: release_type release_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_type
    ADD CONSTRAINT release_type_pkey PRIMARY KEY (id);


--
-- Name: release_type release_type_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_type
    ADD CONSTRAINT release_type_type_key UNIQUE (type);


--
-- Name: single single_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single
    ADD CONSTRAINT single_pkey PRIMARY KEY (id);


--
-- Name: single_song single_song_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_song
    ADD CONSTRAINT single_song_pkey PRIMARY KEY (single_id, song_id);


--
-- Name: song_performer song_performer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song_performer
    ADD CONSTRAINT song_performer_pkey PRIMARY KEY (song_id, performer_id);


--
-- Name: song song_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song
    ADD CONSTRAINT song_pkey PRIMARY KEY (id);


--
-- Name: album_performer album_performer_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album_performer
    ADD CONSTRAINT album_performer_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.album(id) ON DELETE CASCADE;


--
-- Name: album_performer album_performer_performer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album_performer
    ADD CONSTRAINT album_performer_performer_id_fkey FOREIGN KEY (performer_id) REFERENCES public.performer(id) ON DELETE CASCADE;


--
-- Name: album album_release_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_release_type_id_fkey FOREIGN KEY (release_type_id) REFERENCES public.release_type(id) ON DELETE RESTRICT;


--
-- Name: group_musician group_musician_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_musician
    ADD CONSTRAINT group_musician_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.music_group(id) ON DELETE CASCADE;


--
-- Name: group_musician group_musician_musician_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_musician
    ADD CONSTRAINT group_musician_musician_id_fkey FOREIGN KEY (musician_id) REFERENCES public.musician(id) ON DELETE CASCADE;


--
-- Name: performer performer_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performer
    ADD CONSTRAINT performer_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.music_group(id) ON DELETE CASCADE;


--
-- Name: performer performer_musician_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performer
    ADD CONSTRAINT performer_musician_id_fkey FOREIGN KEY (musician_id) REFERENCES public.musician(id) ON DELETE CASCADE;


--
-- Name: producer_album producer_album_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_album
    ADD CONSTRAINT producer_album_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.album(id) ON DELETE CASCADE;


--
-- Name: producer_album producer_album_producer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_album
    ADD CONSTRAINT producer_album_producer_id_fkey FOREIGN KEY (producer_id) REFERENCES public.producer(id) ON DELETE CASCADE;


--
-- Name: producer_song producer_song_producer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_song
    ADD CONSTRAINT producer_song_producer_id_fkey FOREIGN KEY (producer_id) REFERENCES public.producer(id) ON DELETE CASCADE;


--
-- Name: producer_song producer_song_song_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producer_song
    ADD CONSTRAINT producer_song_song_id_fkey FOREIGN KEY (song_id) REFERENCES public.song(id) ON DELETE CASCADE;


--
-- Name: single_song single_song_single_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_song
    ADD CONSTRAINT single_song_single_id_fkey FOREIGN KEY (single_id) REFERENCES public.single(id) ON DELETE CASCADE;


--
-- Name: single_song single_song_song_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_song
    ADD CONSTRAINT single_song_song_id_fkey FOREIGN KEY (song_id) REFERENCES public.song(id) ON DELETE CASCADE;


--
-- Name: song song_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song
    ADD CONSTRAINT song_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.album(id) ON DELETE SET NULL;


--
-- Name: song_performer song_performer_performer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song_performer
    ADD CONSTRAINT song_performer_performer_id_fkey FOREIGN KEY (performer_id) REFERENCES public.performer(id) ON DELETE CASCADE;


--
-- Name: song_performer song_performer_song_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.song_performer
    ADD CONSTRAINT song_performer_song_id_fkey FOREIGN KEY (song_id) REFERENCES public.song(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

