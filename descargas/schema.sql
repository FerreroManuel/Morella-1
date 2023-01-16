--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Ubuntu 14.6-1.pgdg22.04+1)
-- Dumped by pg_dump version 14.6 (Ubuntu 14.6-1.pgdg22.04+1)

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
-- Name: caja; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.caja (
    id integer NOT NULL,
    categoria text NOT NULL,
    descripcion text NOT NULL,
    transaccion text NOT NULL,
    ingreso real,
    egreso real,
    observacion text,
    dia text NOT NULL,
    mes text NOT NULL,
    "año" text NOT NULL,
    cerrada integer DEFAULT 0 NOT NULL,
    id_user integer NOT NULL
);


ALTER TABLE public.caja OWNER TO postgres;

--
-- Name: TABLE caja; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.caja IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.categoria IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.descripcion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.descripcion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.transaccion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.transaccion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.ingreso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.ingreso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.egreso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.egreso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.observacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.observacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.dia; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.dia IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.mes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.mes IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja."año"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja."año" IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.cerrada; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.cerrada IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN caja.id_user; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.caja.id_user IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: caja_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.caja_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.caja_id_seq OWNER TO postgres;

--
-- Name: caja_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.caja_id_seq OWNED BY public.caja.id;


--
-- Name: cat_nichos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cat_nichos (
    id integer NOT NULL,
    categoria text NOT NULL,
    valor_mant_bicon real NOT NULL,
    valor_mant_nob real
);


ALTER TABLE public.cat_nichos OWNER TO postgres;

--
-- Name: TABLE cat_nichos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.cat_nichos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cat_nichos.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cat_nichos.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cat_nichos.categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cat_nichos.categoria IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cat_nichos.valor_mant_bicon; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cat_nichos.valor_mant_bicon IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cat_nichos.valor_mant_nob; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cat_nichos.valor_mant_nob IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: cat_nichos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cat_nichos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cat_nichos_id_seq OWNER TO postgres;

--
-- Name: cat_nichos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cat_nichos_id_seq OWNED BY public.cat_nichos.id;


--
-- Name: cobradores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cobradores (
    id integer NOT NULL,
    cobrador text NOT NULL
);


ALTER TABLE public.cobradores OWNER TO postgres;

--
-- Name: TABLE cobradores; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.cobradores IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cobradores.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cobradores.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cobradores.cobrador; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cobradores.cobrador IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: cobradores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cobradores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cobradores_id_seq OWNER TO postgres;

--
-- Name: cobradores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cobradores_id_seq OWNED BY public.cobradores.id;


--
-- Name: cod_post; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cod_post (
    cp integer NOT NULL,
    localidad text NOT NULL
);


ALTER TABLE public.cod_post OWNER TO postgres;

--
-- Name: TABLE cod_post; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.cod_post IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cod_post.cp; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cod_post.cp IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN cod_post.localidad; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cod_post.localidad IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: cod_post_cp_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cod_post_cp_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cod_post_cp_seq OWNER TO postgres;

--
-- Name: cod_post_cp_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cod_post_cp_seq OWNED BY public.cod_post.cp;


--
-- Name: comercio_fiserv; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comercio_fiserv (
    id integer NOT NULL,
    nro_comercio bigint NOT NULL
);


ALTER TABLE public.comercio_fiserv OWNER TO postgres;

--
-- Name: TABLE comercio_fiserv; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.comercio_fiserv IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comercio_fiserv.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comercio_fiserv.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comercio_fiserv.nro_comercio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comercio_fiserv.nro_comercio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: comercio_fiserv_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comercio_fiserv_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comercio_fiserv_id_seq OWNER TO postgres;

--
-- Name: comercio_fiserv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comercio_fiserv_id_seq OWNED BY public.comercio_fiserv.id;


--
-- Name: comisiones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comisiones (
    cobrador integer NOT NULL,
    rendicion integer NOT NULL,
    recibo integer NOT NULL,
    cobro real NOT NULL,
    comision real NOT NULL
);


ALTER TABLE public.comisiones OWNER TO postgres;

--
-- Name: TABLE comisiones; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.comisiones IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comisiones.cobrador; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comisiones.cobrador IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comisiones.rendicion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comisiones.rendicion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comisiones.recibo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comisiones.recibo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comisiones.cobro; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comisiones.cobro IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN comisiones.comision; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.comisiones.comision IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: datos_complementarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datos_complementarios (
    id_op integer NOT NULL,
    datos text
);


ALTER TABLE public.datos_complementarios OWNER TO postgres;

--
-- Name: TABLE datos_complementarios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.datos_complementarios IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN datos_complementarios.id_op; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.datos_complementarios.id_op IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN datos_complementarios.datos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.datos_complementarios.datos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: datos_complementarios_id_op_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datos_complementarios_id_op_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datos_complementarios_id_op_seq OWNER TO postgres;

--
-- Name: datos_complementarios_id_op_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datos_complementarios_id_op_seq OWNED BY public.datos_complementarios.id_op;


--
-- Name: debitos_automaticos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debitos_automaticos (
    id integer NOT NULL,
    categoria text NOT NULL,
    socio integer NOT NULL,
    operacion integer NOT NULL,
    ingreso real,
    observacion text,
    dia text NOT NULL,
    mes text NOT NULL,
    "año" text NOT NULL,
    id_user integer NOT NULL
);


ALTER TABLE public.debitos_automaticos OWNER TO postgres;

--
-- Name: TABLE debitos_automaticos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.debitos_automaticos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.categoria IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.socio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.socio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.operacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.operacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.ingreso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.ingreso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.observacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.observacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.dia; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.dia IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.mes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.mes IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos."año"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos."año" IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN debitos_automaticos.id_user; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.debitos_automaticos.id_user IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: debitos_automaticos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debitos_automaticos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debitos_automaticos_id_seq OWNER TO postgres;

--
-- Name: debitos_automaticos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.debitos_automaticos_id_seq OWNED BY public.debitos_automaticos.id;


--
-- Name: documentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documentos (
    id_op integer NOT NULL,
    cant_cuotas integer NOT NULL,
    val_cuotas real NOT NULL,
    ult_rec text
);


ALTER TABLE public.documentos OWNER TO postgres;

--
-- Name: TABLE documentos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.documentos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN documentos.id_op; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.documentos.id_op IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN documentos.cant_cuotas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.documentos.cant_cuotas IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN documentos.val_cuotas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.documentos.val_cuotas IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN documentos.ult_rec; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.documentos.ult_rec IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: documentos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documentos_id_seq OWNER TO postgres;

--
-- Name: documentos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documentos_id_seq OWNED BY public.documentos.id_op;


--
-- Name: historial_caja; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.historial_caja (
    id integer NOT NULL,
    categoria text NOT NULL,
    descripcion text NOT NULL,
    transaccion text NOT NULL,
    ingreso real,
    egreso real,
    observacion text,
    id_user_m integer NOT NULL,
    fecha_y_hora_m text NOT NULL
);


ALTER TABLE public.historial_caja OWNER TO postgres;

--
-- Name: TABLE historial_caja; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.historial_caja IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.categoria IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.descripcion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.descripcion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.transaccion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.transaccion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.ingreso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.ingreso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.egreso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.egreso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.observacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.observacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.id_user_m; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.id_user_m IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN historial_caja.fecha_y_hora_m; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.historial_caja.fecha_y_hora_m IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: mail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail (
    id integer NOT NULL,
    etiqueta text NOT NULL,
    mail text NOT NULL,
    smtp_server text NOT NULL,
    smtp_user text NOT NULL,
    smtp_pass text NOT NULL
);


ALTER TABLE public.mail OWNER TO postgres;

--
-- Name: TABLE mail; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.mail IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.etiqueta; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.etiqueta IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.mail; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.mail IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.smtp_server; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.smtp_server IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.smtp_user; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.smtp_user IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN mail.smtp_pass; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mail.smtp_pass IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: mail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_id_seq OWNER TO postgres;

--
-- Name: mail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_id_seq OWNED BY public.mail.id;


--
-- Name: nichos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nichos (
    codigo text NOT NULL,
    panteon integer NOT NULL,
    piso text NOT NULL,
    fila text NOT NULL,
    numero text NOT NULL,
    categoria integer NOT NULL,
    ocupado integer DEFAULT 0 NOT NULL,
    fallecido text
);


ALTER TABLE public.nichos OWNER TO postgres;

--
-- Name: TABLE nichos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.nichos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.codigo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.codigo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.panteon; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.panteon IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.piso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.piso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.fila; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.fila IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.numero; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.numero IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.categoria IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.ocupado; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.ocupado IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN nichos.fallecido; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.nichos.fallecido IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: operaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operaciones (
    id integer NOT NULL,
    socio integer NOT NULL,
    nicho text,
    facturacion text NOT NULL,
    cobrador integer NOT NULL,
    tarjeta bigint,
    ruta integer NOT NULL,
    ult_pago text NOT NULL,
    "ult_año" text,
    fecha_ult_pago text NOT NULL,
    moroso integer DEFAULT 0 NOT NULL,
    cuotas_favor integer DEFAULT 0 NOT NULL,
    ult_rec text NOT NULL,
    paga integer DEFAULT 1 NOT NULL,
    op_cobol integer,
    nombre_alt text,
    domicilio_alt text
);


ALTER TABLE public.operaciones OWNER TO postgres;

--
-- Name: TABLE operaciones; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.operaciones IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.socio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.socio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.nicho; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.nicho IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.facturacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.facturacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.cobrador; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.cobrador IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.tarjeta; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.tarjeta IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.ruta; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.ruta IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.ult_pago; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.ult_pago IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones."ult_año"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones."ult_año" IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.fecha_ult_pago; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.fecha_ult_pago IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.moroso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.moroso IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.cuotas_favor; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.cuotas_favor IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.ult_rec; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.ult_rec IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.paga; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.paga IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.op_cobol; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.op_cobol IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.nombre_alt; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.nombre_alt IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN operaciones.domicilio_alt; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operaciones.domicilio_alt IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: operaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.operaciones_id_seq OWNER TO postgres;

--
-- Name: operaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operaciones_id_seq OWNED BY public.operaciones.id;


--
-- Name: panteones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.panteones (
    id integer NOT NULL,
    panteon text NOT NULL
);


ALTER TABLE public.panteones OWNER TO postgres;

--
-- Name: TABLE panteones; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.panteones IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN panteones.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.panteones.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN panteones.panteon; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.panteones.panteon IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: panteones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.panteones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.panteones_id_seq OWNER TO postgres;

--
-- Name: panteones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.panteones_id_seq OWNED BY public.panteones.id;


--
-- Name: precios_venta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.precios_venta (
    id integer NOT NULL,
    nombre text NOT NULL,
    precio real NOT NULL,
    anticipo real NOT NULL,
    cuotas real NOT NULL
);


ALTER TABLE public.precios_venta OWNER TO postgres;

--
-- Name: TABLE precios_venta; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.precios_venta IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN precios_venta.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.precios_venta.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN precios_venta.nombre; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.precios_venta.nombre IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN precios_venta.precio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.precios_venta.precio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN precios_venta.anticipo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.precios_venta.anticipo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN precios_venta.cuotas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.precios_venta.cuotas IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: precios_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.precios_venta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.precios_venta_id_seq OWNER TO postgres;

--
-- Name: precios_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.precios_venta_id_seq OWNED BY public.precios_venta.id;


--
-- Name: recibos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recibos (
    nro_recibo integer NOT NULL,
    operacion integer NOT NULL,
    periodo text NOT NULL,
    "año" text NOT NULL,
    pago integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.recibos OWNER TO postgres;

--
-- Name: TABLE recibos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.recibos IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN recibos.nro_recibo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.recibos.nro_recibo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN recibos.operacion; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.recibos.operacion IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN recibos.periodo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.recibos.periodo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN recibos."año"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.recibos."año" IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN recibos.pago; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.recibos.pago IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: recibos_nro_recibo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recibos_nro_recibo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recibos_nro_recibo_seq OWNER TO postgres;

--
-- Name: recibos_nro_recibo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recibos_nro_recibo_seq OWNED BY public.recibos.nro_recibo;


--
-- Name: saldo_caja; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.saldo_caja (
    nro_caja integer NOT NULL,
    saldo real,
    fecha_y_hora_cierre text
);


ALTER TABLE public.saldo_caja OWNER TO postgres;

--
-- Name: saldo_caja_nro_caja_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.saldo_caja_nro_caja_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.saldo_caja_nro_caja_seq OWNER TO postgres;

--
-- Name: saldo_caja_nro_caja_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.saldo_caja_nro_caja_seq OWNED BY public.saldo_caja.nro_caja;


--
-- Name: socios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socios (
    nro_socio integer NOT NULL,
    nombre text NOT NULL,
    dni integer NOT NULL,
    telefono_1 text,
    telefono_2 text,
    mail text,
    domicilio text NOT NULL,
    localidad text NOT NULL,
    cod_postal integer NOT NULL,
    fecha_nacimiento text NOT NULL,
    fecha_alta text NOT NULL,
    activo integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.socios OWNER TO postgres;

--
-- Name: TABLE socios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.socios IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.nro_socio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.nro_socio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.nombre; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.nombre IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.dni; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.dni IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.telefono_1; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.telefono_1 IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.telefono_2; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.telefono_2 IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.mail; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.mail IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.domicilio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.domicilio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.localidad; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.localidad IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.cod_postal; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.cod_postal IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.fecha_nacimiento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.fecha_nacimiento IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.fecha_alta; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.fecha_alta IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN socios.activo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.socios.activo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: socios_nro_socio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.socios_nro_socio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socios_nro_socio_seq OWNER TO postgres;

--
-- Name: socios_nro_socio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.socios_nro_socio_seq OWNED BY public.socios.nro_socio;


--
-- Name: sqlite_sequence; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sqlite_sequence (
    name text,
    seq text
);


ALTER TABLE public.sqlite_sequence OWNER TO postgres;

--
-- Name: TABLE sqlite_sequence; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.sqlite_sequence IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN sqlite_sequence.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sqlite_sequence.name IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN sqlite_sequence.seq; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sqlite_sequence.seq IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre text NOT NULL,
    apellido text NOT NULL,
    telefono text NOT NULL,
    domicilio text NOT NULL,
    user_name text NOT NULL,
    pass text NOT NULL,
    privilegios integer NOT NULL,
    activo integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: TABLE usuarios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.usuarios IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.id IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.nombre; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.nombre IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.apellido; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.apellido IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.telefono; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.telefono IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.domicilio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.domicilio IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.user_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.user_name IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.pass; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.pass IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.privilegios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.privilegios IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: COLUMN usuarios.activo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuarios.activo IS 'Morella by MF! Soluciones Informáticas -> https://www.manuelferrero.com.ar';


--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: caja id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caja ALTER COLUMN id SET DEFAULT nextval('public.caja_id_seq'::regclass);


--
-- Name: cat_nichos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cat_nichos ALTER COLUMN id SET DEFAULT nextval('public.cat_nichos_id_seq'::regclass);


--
-- Name: categorias_egresos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_egresos ALTER COLUMN id SET DEFAULT nextval('public.categorias_egresos_id_seq'::regclass);


--
-- Name: categorias_ingresos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_ingresos ALTER COLUMN id SET DEFAULT nextval('public.categorias_ingresos_id_seq'::regclass);


--
-- Name: categorias_prevenir id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_prevenir ALTER COLUMN id SET DEFAULT nextval('public.categorias_prevenir_id_seq'::regclass);


--
-- Name: cobradores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobradores ALTER COLUMN id SET DEFAULT nextval('public.cobradores_id_seq'::regclass);


--
-- Name: cod_post cp; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cod_post ALTER COLUMN cp SET DEFAULT nextval('public.cod_post_cp_seq'::regclass);


--
-- Name: comercio_fiserv id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comercio_fiserv ALTER COLUMN id SET DEFAULT nextval('public.comercio_fiserv_id_seq'::regclass);


--
-- Name: datos_complementarios id_op; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_complementarios ALTER COLUMN id_op SET DEFAULT nextval('public.datos_complementarios_id_op_seq'::regclass);


--
-- Name: debitos_automaticos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debitos_automaticos ALTER COLUMN id SET DEFAULT nextval('public.debitos_automaticos_id_seq'::regclass);


--
-- Name: documentos id_op; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos ALTER COLUMN id_op SET DEFAULT nextval('public.documentos_id_seq'::regclass);


--
-- Name: mail id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail ALTER COLUMN id SET DEFAULT nextval('public.mail_id_seq'::regclass);


--
-- Name: operaciones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones ALTER COLUMN id SET DEFAULT nextval('public.operaciones_id_seq'::regclass);


--
-- Name: panteones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.panteones ALTER COLUMN id SET DEFAULT nextval('public.panteones_id_seq'::regclass);


--
-- Name: planes_prevenir id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes_prevenir ALTER COLUMN id SET DEFAULT nextval('public.planes_prevenir_id_seq'::regclass);


--
-- Name: precios_venta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios_venta ALTER COLUMN id SET DEFAULT nextval('public.precios_venta_id_seq'::regclass);


--
-- Name: recibos nro_recibo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos ALTER COLUMN nro_recibo SET DEFAULT nextval('public.recibos_nro_recibo_seq'::regclass);


--
-- Name: recibos_prevenir nro_recibo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos_prevenir ALTER COLUMN nro_recibo SET DEFAULT nextval('public.recibos_prevenir_nro_recibo_seq'::regclass);


--
-- Name: saldo_caja nro_caja; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo_caja ALTER COLUMN nro_caja SET DEFAULT nextval('public.saldo_caja_nro_caja_seq'::regclass);


--
-- Name: socios nro_socio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socios ALTER COLUMN nro_socio SET DEFAULT nextval('public.socios_nro_socio_seq'::regclass);


--
-- Name: solicitudes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes ALTER COLUMN id SET DEFAULT nextval('public.solicitudes_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: caja caja_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caja
    ADD CONSTRAINT caja_pk PRIMARY KEY (id);


--
-- Name: categorias_egresos categorias_egresos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_egresos
    ADD CONSTRAINT categorias_egresos_pkey PRIMARY KEY (id);


--
-- Name: categorias_ingresos categorias_ingresos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_ingresos
    ADD CONSTRAINT categorias_ingresos_pkey PRIMARY KEY (id);


--
-- Name: categorias_prevenir categorias_prevenir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_prevenir
    ADD CONSTRAINT categorias_prevenir_pk PRIMARY KEY (id);


--
-- Name: cobradores cobradores_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobradores
    ADD CONSTRAINT cobradores_pk PRIMARY KEY (id);


--
-- Name: comercio_fiserv comercio_fiserv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comercio_fiserv
    ADD CONSTRAINT comercio_fiserv_pkey PRIMARY KEY (id);


--
-- Name: debitos_automaticos debitos_automaticos_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debitos_automaticos
    ADD CONSTRAINT debitos_automaticos_pk PRIMARY KEY (id);


--
-- Name: operaciones operaciones_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT operaciones_id_key UNIQUE (id);


--
-- Name: panteones panteones_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.panteones
    ADD CONSTRAINT panteones_pk PRIMARY KEY (id);


--
-- Name: mail pk_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail
    ADD CONSTRAINT pk_id PRIMARY KEY (id);


--
-- Name: planes_prevenir planes_prevenir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes_prevenir
    ADD CONSTRAINT planes_prevenir_pk PRIMARY KEY (id);


--
-- Name: recibos recibos_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos
    ADD CONSTRAINT recibos_pk PRIMARY KEY (nro_recibo);


--
-- Name: recibos_prevenir recibos_prevenir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos_prevenir
    ADD CONSTRAINT recibos_prevenir_pk PRIMARY KEY (nro_recibo);


--
-- Name: saldo_caja saldo_caja_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo_caja
    ADD CONSTRAINT saldo_caja_pkey PRIMARY KEY (nro_caja);


--
-- Name: socios socios_nro_socio_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socios
    ADD CONSTRAINT socios_nro_socio_key UNIQUE (nro_socio);


--
-- Name: solicitudes solicitudes_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes
    ADD CONSTRAINT solicitudes_pk PRIMARY KEY (id);


--
-- Name: cat_nichos sqlite_autoindex_cat_nichos_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cat_nichos
    ADD CONSTRAINT sqlite_autoindex_cat_nichos_1 PRIMARY KEY (categoria, id);


--
-- Name: cod_post sqlite_autoindex_cod_post_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cod_post
    ADD CONSTRAINT sqlite_autoindex_cod_post_1 PRIMARY KEY (cp);


--
-- Name: datos_complementarios sqlite_autoindex_datos_complementarios_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_complementarios
    ADD CONSTRAINT sqlite_autoindex_datos_complementarios_1 PRIMARY KEY (id_op);


--
-- Name: nichos sqlite_autoindex_nichos_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nichos
    ADD CONSTRAINT sqlite_autoindex_nichos_1 PRIMARY KEY (codigo);


--
-- Name: operaciones sqlite_autoindex_operaciones_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT sqlite_autoindex_operaciones_1 PRIMARY KEY (id);


--
-- Name: precios_venta sqlite_autoindex_precios_venta_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios_venta
    ADD CONSTRAINT sqlite_autoindex_precios_venta_1 PRIMARY KEY (nombre, id);


--
-- Name: socios sqlite_autoindex_socios_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socios
    ADD CONSTRAINT sqlite_autoindex_socios_1 PRIMARY KEY (dni, nro_socio);


--
-- Name: usuarios sqlite_autoindex_usuarios_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT sqlite_autoindex_usuarios_1 PRIMARY KEY (user_name, id);


--
-- Name: mail u_etiqueta; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail
    ADD CONSTRAINT u_etiqueta UNIQUE (etiqueta);


--
-- Name: usuarios u_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT u_id UNIQUE (id);


--
-- Name: cat_nichos u_id_cat; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cat_nichos
    ADD CONSTRAINT u_id_cat UNIQUE (id);


--
-- Name: mail u_smtp_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail
    ADD CONSTRAINT u_smtp_user UNIQUE (smtp_user);


--
-- Name: datos_complementarios datos_complementarios_id_op_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_complementarios
    ADD CONSTRAINT datos_complementarios_id_op_fkey FOREIGN KEY (id_op) REFERENCES public.operaciones(id) NOT VALID;


--
-- Name: nichos fk_categoria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nichos
    ADD CONSTRAINT fk_categoria FOREIGN KEY (categoria) REFERENCES public.cat_nichos(id);


--
-- Name: comisiones fk_cod_post_cobradores_1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comisiones
    ADD CONSTRAINT fk_cod_post_cobradores_1 FOREIGN KEY (cobrador) REFERENCES public.cobradores(id);


--
-- Name: comisiones fk_cod_post_recibos_0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comisiones
    ADD CONSTRAINT fk_cod_post_recibos_0 FOREIGN KEY (recibo) REFERENCES public.recibos(nro_recibo);


--
-- Name: historial_caja fk_id_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_caja
    ADD CONSTRAINT fk_id_user FOREIGN KEY (id_user_m) REFERENCES public.usuarios(id);


--
-- Name: debitos_automaticos fk_operacion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debitos_automaticos
    ADD CONSTRAINT fk_operacion FOREIGN KEY (operacion) REFERENCES public.operaciones(id);


--
-- Name: operaciones fk_operaciones_cobrador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_cobrador FOREIGN KEY (cobrador) REFERENCES public.cobradores(id);


--
-- Name: operaciones fk_operaciones_nicho; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_nicho FOREIGN KEY (nicho) REFERENCES public.nichos(codigo);


--
-- Name: operaciones fk_operaciones_socio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_socio FOREIGN KEY (socio) REFERENCES public.socios(nro_socio);


--
-- Name: nichos fk_panteon; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nichos
    ADD CONSTRAINT fk_panteon FOREIGN KEY (panteon) REFERENCES public.panteones(id);


--
-- Name: recibos fk_recibos_operaciones; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos
    ADD CONSTRAINT fk_recibos_operaciones FOREIGN KEY (operacion) REFERENCES public.operaciones(id);


--
-- Name: soc_x_sol fk_recibos_prevenir_solicitudes_1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soc_x_sol
    ADD CONSTRAINT fk_recibos_prevenir_solicitudes_1 FOREIGN KEY (solicitud) REFERENCES public.solicitudes(id);


--
-- Name: recibos_prevenir fk_recibos_solicitudes_0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recibos_prevenir
    ADD CONSTRAINT fk_recibos_solicitudes_0 FOREIGN KEY (solicitud) REFERENCES public.solicitudes(id);


--
-- Name: soc_x_sol fk_soc_x_sol_socio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soc_x_sol
    ADD CONSTRAINT fk_soc_x_sol_socio FOREIGN KEY (socio) REFERENCES public.socios(nro_socio);


--
-- Name: debitos_automaticos fk_socio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debitos_automaticos
    ADD CONSTRAINT fk_socio FOREIGN KEY (socio) REFERENCES public.socios(nro_socio);


--
-- Name: solicitudes fk_socios_cobradores_1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes
    ADD CONSTRAINT fk_socios_cobradores_1 FOREIGN KEY (cobrador) REFERENCES public.cobradores(id);


--
-- Name: socios fk_socios_cp; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socios
    ADD CONSTRAINT fk_socios_cp FOREIGN KEY (cod_postal) REFERENCES public.cod_post(cp);


--
-- Name: solicitudes fk_socios_planes_prevenir_0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes
    ADD CONSTRAINT fk_socios_planes_prevenir_0 FOREIGN KEY (plan) REFERENCES public.planes_prevenir(id);


--
-- Name: documentos pk_documentos_id_op; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos
    ADD CONSTRAINT pk_documentos_id_op FOREIGN KEY (id_op) REFERENCES public.operaciones(id) NOT VALID;


--
-- PostgreSQL database dump complete
--

