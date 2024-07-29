--
-- PostgreSQL database dump
--

-- Dumped from database version 13.15 (Debian 13.15-1.pgdg120+1)
-- Dumped by pg_dump version 13.15 (Debian 13.15-1.pgdg120+1)

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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO admin;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: recipes_favoriterecipe; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_favoriterecipe (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    recipe_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.recipes_favoriterecipe OWNER TO admin;

--
-- Name: recipes_favoriterecipe_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_favoriterecipe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_favoriterecipe_id_seq OWNER TO admin;

--
-- Name: recipes_favoriterecipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_favoriterecipe_id_seq OWNED BY public.recipes_favoriterecipe.id;


--
-- Name: recipes_ingredient; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_ingredient (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    measurement_unit character varying(200) NOT NULL
);


ALTER TABLE public.recipes_ingredient OWNER TO admin;

--
-- Name: recipes_ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_ingredient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_ingredient_id_seq OWNER TO admin;

--
-- Name: recipes_ingredient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_ingredient_id_seq OWNED BY public.recipes_ingredient.id;


--
-- Name: recipes_recipe; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_recipe (
    id bigint NOT NULL,
    name character varying(199) NOT NULL,
    image character varying(100),
    text text NOT NULL,
    cooking_time smallint NOT NULL,
    pub_date timestamp with time zone,
    author_id bigint,
    CONSTRAINT recipes_recipe_cooking_time_check CHECK ((cooking_time >= 0))
);


ALTER TABLE public.recipes_recipe OWNER TO admin;

--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_recipe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_recipe_id_seq OWNER TO admin;

--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_recipe_id_seq OWNED BY public.recipes_recipe.id;


--
-- Name: recipes_recipe_tags; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_recipe_tags (
    id bigint NOT NULL,
    recipe_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.recipes_recipe_tags OWNER TO admin;

--
-- Name: recipes_recipe_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_recipe_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_recipe_tags_id_seq OWNER TO admin;

--
-- Name: recipes_recipe_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_recipe_tags_id_seq OWNED BY public.recipes_recipe_tags.id;


--
-- Name: recipes_recipeingredients; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_recipeingredients (
    id bigint NOT NULL,
    amount smallint NOT NULL,
    ingredient_id bigint NOT NULL,
    recipe_id bigint NOT NULL,
    CONSTRAINT recipes_recipeingredients_amount_check CHECK ((amount >= 0))
);


ALTER TABLE public.recipes_recipeingredients OWNER TO admin;

--
-- Name: recipes_recipeingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_recipeingredients_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_recipeingredients_id_seq OWNER TO admin;

--
-- Name: recipes_recipeingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_recipeingredients_id_seq OWNED BY public.recipes_recipeingredients.id;


--
-- Name: recipes_shoppingcart; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_shoppingcart (
    id bigint NOT NULL,
    recipe_id bigint,
    user_id bigint NOT NULL
);


ALTER TABLE public.recipes_shoppingcart OWNER TO admin;

--
-- Name: recipes_shoppingcart_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_shoppingcart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_shoppingcart_id_seq OWNER TO admin;

--
-- Name: recipes_shoppingcart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_shoppingcart_id_seq OWNED BY public.recipes_shoppingcart.id;


--
-- Name: recipes_subscribe; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_subscribe (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    author_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.recipes_subscribe OWNER TO admin;

--
-- Name: recipes_subscribe_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_subscribe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_subscribe_id_seq OWNER TO admin;

--
-- Name: recipes_subscribe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_subscribe_id_seq OWNED BY public.recipes_subscribe.id;


--
-- Name: recipes_tag; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.recipes_tag (
    id bigint NOT NULL,
    name character varying(25) NOT NULL,
    color character varying(25) NOT NULL,
    slug character varying(25) NOT NULL
);


ALTER TABLE public.recipes_tag OWNER TO admin;

--
-- Name: recipes_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.recipes_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_tag_id_seq OWNER TO admin;

--
-- Name: recipes_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.recipes_tag_id_seq OWNED BY public.recipes_tag.id;


--
-- Name: users_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    avatar character varying(100)
);


ALTER TABLE public.users_user OWNER TO admin;

--
-- Name: users_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_user_groups OWNER TO admin;

--
-- Name: users_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_groups_id_seq OWNER TO admin;

--
-- Name: users_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_user_groups_id_seq OWNED BY public.users_user_groups.id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO admin;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users_user.id;


--
-- Name: users_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_user_permissions OWNER TO admin;

--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_user_permissions_id_seq OWNER TO admin;

--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_user_user_permissions_id_seq OWNED BY public.users_user_user_permissions.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: recipes_favoriterecipe id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_favoriterecipe ALTER COLUMN id SET DEFAULT nextval('public.recipes_favoriterecipe_id_seq'::regclass);


--
-- Name: recipes_ingredient id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_ingredient ALTER COLUMN id SET DEFAULT nextval('public.recipes_ingredient_id_seq'::regclass);


--
-- Name: recipes_recipe id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe ALTER COLUMN id SET DEFAULT nextval('public.recipes_recipe_id_seq'::regclass);


--
-- Name: recipes_recipe_tags id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe_tags ALTER COLUMN id SET DEFAULT nextval('public.recipes_recipe_tags_id_seq'::regclass);


--
-- Name: recipes_recipeingredients id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipeingredients ALTER COLUMN id SET DEFAULT nextval('public.recipes_recipeingredients_id_seq'::regclass);


--
-- Name: recipes_shoppingcart id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_shoppingcart ALTER COLUMN id SET DEFAULT nextval('public.recipes_shoppingcart_id_seq'::regclass);


--
-- Name: recipes_subscribe id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_subscribe ALTER COLUMN id SET DEFAULT nextval('public.recipes_subscribe_id_seq'::regclass);


--
-- Name: recipes_tag id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_tag ALTER COLUMN id SET DEFAULT nextval('public.recipes_tag_id_seq'::regclass);


--
-- Name: users_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user ALTER COLUMN id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: users_user_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups ALTER COLUMN id SET DEFAULT nextval('public.users_user_groups_id_seq'::regclass);


--
-- Name: users_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.users_user_user_permissions_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add token	7	add_tokenproxy
26	Can change token	7	change_tokenproxy
27	Can delete token	7	delete_tokenproxy
28	Can view token	7	view_tokenproxy
29	Can add Пользователь	8	add_user
30	Can change Пользователь	8	change_user
31	Can delete Пользователь	8	delete_user
32	Can view Пользователь	8	view_user
33	Can add Избранный рецепт	9	add_favoriterecipe
34	Can change Избранный рецепт	9	change_favoriterecipe
35	Can delete Избранный рецепт	9	delete_favoriterecipe
36	Can view Избранный рецепт	9	view_favoriterecipe
37	Can add Ингредиент	10	add_ingredient
38	Can change Ингредиент	10	change_ingredient
39	Can delete Ингредиент	10	delete_ingredient
40	Can view Ингредиент	10	view_ingredient
41	Can add Рецепт	11	add_recipe
42	Can change Рецепт	11	change_recipe
43	Can delete Рецепт	11	delete_recipe
44	Can view Рецепт	11	view_recipe
45	Can add Количество ингредиента в рецепте	12	add_recipeingredients
46	Can change Количество ингредиента в рецепте	12	change_recipeingredients
47	Can delete Количество ингредиента в рецепте	12	delete_recipeingredients
48	Can view Количество ингредиента в рецепте	12	view_recipeingredients
49	Can add Покупка	13	add_shoppingcart
50	Can change Покупка	13	change_shoppingcart
51	Can delete Покупка	13	delete_shoppingcart
52	Can view Покупка	13	view_shoppingcart
53	Can add Подписка	14	add_subscribe
54	Can change Подписка	14	change_subscribe
55	Can delete Подписка	14	delete_subscribe
56	Can view Подписка	14	view_subscribe
57	Can add Тег	15	add_tag
58	Can change Тег	15	change_tag
59	Can delete Тег	15	delete_tag
60	Can view Тег	15	view_tag
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2024-07-27 05:30:59.04815+00	1	tag1 (FFFF00)	1	[{"added": {}}]	15	1
2	2024-07-27 05:31:05.783839+00	2	tag2 (FFFFFF)	1	[{"added": {}}]	15	1
3	2024-07-27 05:31:12.869388+00	3	tag3 (FF0000)	1	[{"added": {}}]	15	1
4	2024-07-27 05:31:28.036163+00	1	гречка, гр.	1	[{"added": {}}]	10	1
5	2024-07-27 05:31:34.331714+00	2	картошка, гр.	1	[{"added": {}}]	10	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	authtoken	token
7	authtoken	tokenproxy
8	users	user
9	recipes	favoriterecipe
10	recipes	ingredient
11	recipes	recipe
12	recipes	recipeingredients
13	recipes	shoppingcart
14	recipes	subscribe
15	recipes	tag
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-07-27 05:23:37.483944+00
2	contenttypes	0002_remove_content_type_name	2024-07-27 05:23:37.533426+00
3	auth	0001_initial	2024-07-27 05:23:37.930416+00
4	auth	0002_alter_permission_name_max_length	2024-07-27 05:23:37.946773+00
5	auth	0003_alter_user_email_max_length	2024-07-27 05:23:37.967069+00
6	auth	0004_alter_user_username_opts	2024-07-27 05:23:37.994597+00
7	auth	0005_alter_user_last_login_null	2024-07-27 05:23:38.019059+00
8	auth	0006_require_contenttypes_0002	2024-07-27 05:23:38.028532+00
9	auth	0007_alter_validators_add_error_messages	2024-07-27 05:23:38.054462+00
10	auth	0008_alter_user_username_max_length	2024-07-27 05:23:38.07882+00
11	auth	0009_alter_user_last_name_max_length	2024-07-27 05:23:38.101557+00
12	auth	0010_alter_group_name_max_length	2024-07-27 05:23:38.122863+00
13	auth	0011_update_proxy_permissions	2024-07-27 05:23:38.145985+00
14	auth	0012_alter_user_first_name_max_length	2024-07-27 05:23:38.191496+00
15	users	0001_initial	2024-07-27 05:23:38.605887+00
16	admin	0001_initial	2024-07-27 05:23:38.713842+00
17	admin	0002_logentry_remove_auto_add	2024-07-27 05:23:38.742108+00
18	admin	0003_logentry_add_action_flag_choices	2024-07-27 05:23:38.771352+00
19	authtoken	0001_initial	2024-07-27 05:23:38.869304+00
20	authtoken	0002_auto_20160226_1747	2024-07-27 05:23:38.985464+00
21	authtoken	0003_tokenproxy	2024-07-27 05:23:38.998654+00
22	recipes	0001_initial	2024-07-27 05:23:39.328221+00
23	recipes	0002_initial	2024-07-27 05:23:40.80898+00
24	sessions	0001_initial	2024-07-27 05:23:40.904725+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
6lll345nm1h2nv4qzge48u8qd52dp7ak	.eJxVjEEOwiAQRe_C2hAYKBSX7j0DmTKDVA0kpV0Z765NutDtf-_9l4i4rSVunZc4kzgLLU6_24TpwXUHdMd6azK1ui7zJHdFHrTLayN-Xg7376BgL98awIPSo1EJNZM2lJPyaWBrx0AELocQcg4GsvXAms2EPLg8JIUOrHfi_QHUrjep:1sXa0t:etV4HJeRvSB9ECQyFCErUua4g3StCYKbNDI61eLox90	2024-08-10 05:30:39.89781+00
\.


--
-- Data for Name: recipes_favoriterecipe; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_favoriterecipe (id, created_at, recipe_id, user_id) FROM stdin;
\.


--
-- Data for Name: recipes_ingredient; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_ingredient (id, name, measurement_unit) FROM stdin;
1	гречка	гр
2	картошка	гр
\.


--
-- Data for Name: recipes_recipe; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_recipe (id, name, image, text, cooking_time, pub_date, author_id) FROM stdin;
\.


--
-- Data for Name: recipes_recipe_tags; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_recipe_tags (id, recipe_id, tag_id) FROM stdin;
\.


--
-- Data for Name: recipes_recipeingredients; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_recipeingredients (id, amount, ingredient_id, recipe_id) FROM stdin;
\.


--
-- Data for Name: recipes_shoppingcart; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_shoppingcart (id, recipe_id, user_id) FROM stdin;
\.


--
-- Data for Name: recipes_subscribe; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_subscribe (id, created_at, author_id, user_id) FROM stdin;
\.


--
-- Data for Name: recipes_tag; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.recipes_tag (id, name, color, slug) FROM stdin;
1	tag1	FFFF00	tag1
2	tag2	FFFFFF	tag2
3	tag3	FF0000	tag3
\.


--
-- Data for Name: users_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user (id, password, last_login, is_superuser, username, is_staff, is_active, date_joined, email, first_name, last_name, avatar) FROM stdin;
1	pbkdf2_sha256$260000$UCoK56e1AH1kzeYmRFvFw6$JYvxyF1Il+0E2VZu1mjAiwc/VVw60X+hpeMblX8oIvk=	2024-07-27 05:30:39.889402+00	t	test_username	t	t	2024-07-27 05:24:59.499564+00	123@mail.ru	RRR	PPP	
\.


--
-- Data for Name: users_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 5, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 24, true);


--
-- Name: recipes_favoriterecipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_favoriterecipe_id_seq', 1, false);


--
-- Name: recipes_ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_ingredient_id_seq', 2, true);


--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_recipe_id_seq', 1, false);


--
-- Name: recipes_recipe_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_recipe_tags_id_seq', 1, false);


--
-- Name: recipes_recipeingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_recipeingredients_id_seq', 1, false);


--
-- Name: recipes_shoppingcart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_shoppingcart_id_seq', 1, false);


--
-- Name: recipes_subscribe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_subscribe_id_seq', 1, false);


--
-- Name: recipes_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.recipes_tag_id_seq', 3, true);


--
-- Name: users_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_groups_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: recipes_favoriterecipe recipes_favoriterecipe_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_favoriterecipe
    ADD CONSTRAINT recipes_favoriterecipe_pkey PRIMARY KEY (id);


--
-- Name: recipes_favoriterecipe recipes_favoriterecipe_user_id_recipe_id_cfd85391_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_favoriterecipe
    ADD CONSTRAINT recipes_favoriterecipe_user_id_recipe_id_cfd85391_uniq UNIQUE (user_id, recipe_id);


--
-- Name: recipes_ingredient recipes_ingredient_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_ingredient
    ADD CONSTRAINT recipes_ingredient_pkey PRIMARY KEY (id);


--
-- Name: recipes_recipe recipes_recipe_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe
    ADD CONSTRAINT recipes_recipe_pkey PRIMARY KEY (id);


--
-- Name: recipes_recipe_tags recipes_recipe_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe_tags
    ADD CONSTRAINT recipes_recipe_tags_pkey PRIMARY KEY (id);


--
-- Name: recipes_recipe_tags recipes_recipe_tags_recipe_id_tag_id_233281ac_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe_tags
    ADD CONSTRAINT recipes_recipe_tags_recipe_id_tag_id_233281ac_uniq UNIQUE (recipe_id, tag_id);


--
-- Name: recipes_recipeingredients recipes_recipeingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipeingredients
    ADD CONSTRAINT recipes_recipeingredients_pkey PRIMARY KEY (id);


--
-- Name: recipes_shoppingcart recipes_shoppingcart_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_shoppingcart
    ADD CONSTRAINT recipes_shoppingcart_pkey PRIMARY KEY (id);


--
-- Name: recipes_subscribe recipes_subscribe_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_subscribe
    ADD CONSTRAINT recipes_subscribe_pkey PRIMARY KEY (id);


--
-- Name: recipes_subscribe recipes_subscribe_user_id_author_id_a5e19cbf_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_subscribe
    ADD CONSTRAINT recipes_subscribe_user_id_author_id_a5e19cbf_uniq UNIQUE (user_id, author_id);


--
-- Name: recipes_tag recipes_tag_color_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_tag
    ADD CONSTRAINT recipes_tag_color_key UNIQUE (color);


--
-- Name: recipes_tag recipes_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_tag
    ADD CONSTRAINT recipes_tag_name_key UNIQUE (name);


--
-- Name: recipes_tag recipes_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_tag
    ADD CONSTRAINT recipes_tag_pkey PRIMARY KEY (id);


--
-- Name: recipes_tag recipes_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_tag
    ADD CONSTRAINT recipes_tag_slug_key UNIQUE (slug);


--
-- Name: recipes_shoppingcart unique_shopping_cart; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_shoppingcart
    ADD CONSTRAINT unique_shopping_cart UNIQUE (user_id, recipe_id);


--
-- Name: users_user users_user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_email_key UNIQUE (email);


--
-- Name: users_user_groups users_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_pkey PRIMARY KEY (id);


--
-- Name: users_user_groups users_user_groups_user_id_group_id_b88eab82_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_group_id_b88eab82_uniq UNIQUE (user_id, group_id);


--
-- Name: users_user users_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_pkey PRIMARY KEY (id);


--
-- Name: users_user_user_permissions users_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_permission_id_43338c45_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_permission_id_43338c45_uniq UNIQUE (user_id, permission_id);


--
-- Name: users_user users_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_username_key UNIQUE (username);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: recipes_favoriterecipe_recipe_id_4f336171; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_favoriterecipe_recipe_id_4f336171 ON public.recipes_favoriterecipe USING btree (recipe_id);


--
-- Name: recipes_favoriterecipe_user_id_6da7b3e0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_favoriterecipe_user_id_6da7b3e0 ON public.recipes_favoriterecipe USING btree (user_id);


--
-- Name: recipes_recipe_author_id_7274f74b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_recipe_author_id_7274f74b ON public.recipes_recipe USING btree (author_id);


--
-- Name: recipes_recipe_tags_recipe_id_e15a4132; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_recipe_tags_recipe_id_e15a4132 ON public.recipes_recipe_tags USING btree (recipe_id);


--
-- Name: recipes_recipe_tags_tag_id_6fe328c4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_recipe_tags_tag_id_6fe328c4 ON public.recipes_recipe_tags USING btree (tag_id);


--
-- Name: recipes_recipeingredients_ingredient_id_4fea9917; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_recipeingredients_ingredient_id_4fea9917 ON public.recipes_recipeingredients USING btree (ingredient_id);


--
-- Name: recipes_recipeingredients_recipe_id_2ae3da78; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_recipeingredients_recipe_id_2ae3da78 ON public.recipes_recipeingredients USING btree (recipe_id);


--
-- Name: recipes_shoppingcart_recipe_id_7b01d980; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_shoppingcart_recipe_id_7b01d980 ON public.recipes_shoppingcart USING btree (recipe_id);


--
-- Name: recipes_shoppingcart_user_id_9cf94f11; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_shoppingcart_user_id_9cf94f11 ON public.recipes_shoppingcart USING btree (user_id);


--
-- Name: recipes_subscribe_author_id_221fab30; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_subscribe_author_id_221fab30 ON public.recipes_subscribe USING btree (author_id);


--
-- Name: recipes_subscribe_user_id_a873ddeb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_subscribe_user_id_a873ddeb ON public.recipes_subscribe USING btree (user_id);


--
-- Name: recipes_tag_color_80798f0a_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_tag_color_80798f0a_like ON public.recipes_tag USING btree (color varchar_pattern_ops);


--
-- Name: recipes_tag_name_fdbc724f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_tag_name_fdbc724f_like ON public.recipes_tag USING btree (name varchar_pattern_ops);


--
-- Name: recipes_tag_slug_baa21000_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX recipes_tag_slug_baa21000_like ON public.recipes_tag USING btree (slug varchar_pattern_ops);


--
-- Name: users_user_email_243f6e77_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_email_243f6e77_like ON public.users_user USING btree (email varchar_pattern_ops);


--
-- Name: users_user_groups_group_id_9afc8d0e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_group_id_9afc8d0e ON public.users_user_groups USING btree (group_id);


--
-- Name: users_user_groups_user_id_5f6f5a90; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_user_id_5f6f5a90 ON public.users_user_groups USING btree (user_id);


--
-- Name: users_user_user_permissions_permission_id_0b93982e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_permission_id_0b93982e ON public.users_user_user_permissions USING btree (permission_id);


--
-- Name: users_user_user_permissions_user_id_20aca447; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_user_id_20aca447 ON public.users_user_user_permissions USING btree (user_id);


--
-- Name: users_user_username_06e46fe6_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_username_06e46fe6_like ON public.users_user USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_favoriterecipe recipes_favoriterecipe_recipe_id_4f336171_fk_recipes_recipe_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_favoriterecipe
    ADD CONSTRAINT recipes_favoriterecipe_recipe_id_4f336171_fk_recipes_recipe_id FOREIGN KEY (recipe_id) REFERENCES public.recipes_recipe(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_favoriterecipe recipes_favoriterecipe_user_id_6da7b3e0_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_favoriterecipe
    ADD CONSTRAINT recipes_favoriterecipe_user_id_6da7b3e0_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_recipe recipes_recipe_author_id_7274f74b_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe
    ADD CONSTRAINT recipes_recipe_author_id_7274f74b_fk_users_user_id FOREIGN KEY (author_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_recipe_tags recipes_recipe_tags_recipe_id_e15a4132_fk_recipes_recipe_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe_tags
    ADD CONSTRAINT recipes_recipe_tags_recipe_id_e15a4132_fk_recipes_recipe_id FOREIGN KEY (recipe_id) REFERENCES public.recipes_recipe(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_recipe_tags recipes_recipe_tags_tag_id_6fe328c4_fk_recipes_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipe_tags
    ADD CONSTRAINT recipes_recipe_tags_tag_id_6fe328c4_fk_recipes_tag_id FOREIGN KEY (tag_id) REFERENCES public.recipes_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_recipeingredients recipes_recipeingred_ingredient_id_4fea9917_fk_recipes_i; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipeingredients
    ADD CONSTRAINT recipes_recipeingred_ingredient_id_4fea9917_fk_recipes_i FOREIGN KEY (ingredient_id) REFERENCES public.recipes_ingredient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_recipeingredients recipes_recipeingred_recipe_id_2ae3da78_fk_recipes_r; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_recipeingredients
    ADD CONSTRAINT recipes_recipeingred_recipe_id_2ae3da78_fk_recipes_r FOREIGN KEY (recipe_id) REFERENCES public.recipes_recipe(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_shoppingcart recipes_shoppingcart_recipe_id_7b01d980_fk_recipes_recipe_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_shoppingcart
    ADD CONSTRAINT recipes_shoppingcart_recipe_id_7b01d980_fk_recipes_recipe_id FOREIGN KEY (recipe_id) REFERENCES public.recipes_recipe(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_shoppingcart recipes_shoppingcart_user_id_9cf94f11_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_shoppingcart
    ADD CONSTRAINT recipes_shoppingcart_user_id_9cf94f11_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_subscribe recipes_subscribe_author_id_221fab30_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_subscribe
    ADD CONSTRAINT recipes_subscribe_author_id_221fab30_fk_users_user_id FOREIGN KEY (author_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: recipes_subscribe recipes_subscribe_user_id_a873ddeb_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.recipes_subscribe
    ADD CONSTRAINT recipes_subscribe_user_id_a873ddeb_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_group_id_9afc8d0e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_group_id_9afc8d0e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_user_id_5f6f5a90_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_5f6f5a90_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_perm_permission_id_0b93982e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_perm_permission_id_0b93982e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_20aca447_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_20aca447_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

