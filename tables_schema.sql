--
-- PostgreSQL database dump
--

\restrict lrLYQIqy4Kb9Ga61OiQflXIgBAyEy4xpwiiJ800UXgBdsdTcsvbo9wtMr40FqGS

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

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
-- Name: addresses; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.addresses (
    id integer NOT NULL,
    customer_id integer,
    address_line1 text,
    region character varying(100),
    state_province character varying(100),
    city character varying(100),
    district character varying(100),
    sub_district character varying(100),
    address character varying(100),
    zip_code character varying(100),
    is_default boolean DEFAULT false NOT NULL
);


ALTER TABLE public.addresses OWNER TO ekky;

--
-- Name: addresses_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.addresses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.addresses_id_seq OWNER TO ekky;

--
-- Name: addresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.addresses_id_seq OWNED BY public.addresses.id;


--
-- Name: brands; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.brands (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.brands OWNER TO ekky;

--
-- Name: brands_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.brands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.brands_id_seq OWNER TO ekky;

--
-- Name: brands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.brands_id_seq OWNED BY public.brands.id;


--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.cart_items (
    id integer NOT NULL,
    product_id integer,
    customer_id integer,
    quantity integer DEFAULT 1 NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cart_items OWNER TO ekky;

--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_items_id_seq OWNER TO ekky;

--
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE public.categories OWNER TO ekky;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO ekky;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    hash_password character varying(255) NOT NULL,
    phone_number character varying(30) NOT NULL,
    email character varying(50) NOT NULL,
    religion character varying(25),
    gender character varying(25),
    profile_picture character varying(255),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.customers OWNER TO ekky;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO ekky;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer NOT NULL,
    price_at_purchase numeric(15,2)
);


ALTER TABLE public.order_items OWNER TO ekky;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO ekky;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.orders OWNER TO ekky;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO ekky;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    amount numeric(15,2) NOT NULL,
    payment_date timestamp with time zone DEFAULT now() NOT NULL,
    status character varying(20) NOT NULL,
    order_id integer NOT NULL
);


ALTER TABLE public.payments OWNER TO ekky;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO ekky;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: ekky
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(15,2) NOT NULL,
    description text,
    sku character varying(50) NOT NULL,
    quantity_stock integer DEFAULT 0 NOT NULL,
    weight numeric(10,2),
    length numeric(10,2),
    width numeric(10,2),
    created_at timestamp with time zone DEFAULT now(),
    brand_id integer,
    category_id integer,
    CONSTRAINT check_stock_non_negative CHECK ((quantity_stock >= 0))
);


ALTER TABLE public.products OWNER TO ekky;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: ekky
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO ekky;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ekky
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: addresses id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);


--
-- Name: brands id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.brands ALTER COLUMN id SET DEFAULT nextval('public.brands_id_seq'::regclass);


--
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: customers customers_email_key; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_sku_key; Type: CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_sku_key UNIQUE (sku);


--
-- Name: addresses addresses_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: cart_items fk_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: orders fk_customer_orders_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_customer_orders_id FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: order_items fk_orders_order_item_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_orders_order_item_id FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: payments fk_payments_orders_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT fk_payments_orders_id FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE RESTRICT;


--
-- Name: cart_items fk_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: order_items fk_product_order_item_id; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_product_order_item_id FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- Name: products products_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ekky
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- PostgreSQL database dump complete
--

\unrestrict lrLYQIqy4Kb9Ga61OiQflXIgBAyEy4xpwiiJ800UXgBdsdTcsvbo9wtMr40FqGS

