-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/T88cXV
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE us_accident (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    VE_TOTAL int   NOT NULL,
    PVH_INVL int   NOT NULL,
    PEDS int   NOT NULL,
    PERSONS int   NOT NULL,
    PERMVIT int   NOT NULL,
    PERNOTMVIT int   NOT NULL,
    COUNTYNAME varchar(50)   NOT NULL,
    CITYNAME varchar(50)   NOT NULL,
    DAY_i int   NOT NULL,
    MONTH_i int   NOT NULL,
    MONTH_iNAME varchar(50)   NOT NULL,
    YEAR_i int   NOT NULL,
    DAY_i_WEEKNAME varchar(50)   NOT NULL,
    HOURNAME varchar(50)   NOT NULL,
    MINUTE_i int   NOT NULL,
    NHSNAME varchar(50)   NOT NULL,
    ROUTENAME varchar(50)   NOT NULL,
    TWAY_ID varchar(50)   NOT NULL,
    RUR_URBNAME varchar(50)   NOT NULL,
    FUNC_SYSNAME varchar(50)   NOT NULL,
    RD_OWNERNAME varchar(50)   NOT NULL,
    WEATHERNAME varchar(50)   NOT NULL,
    LATITUDE int   NOT NULL,
    LONGITUD int   NOT NULL,
    SP_JURNAME varchar(50)   NOT NULL,
    HARM_EVNAME varchar(50)   NOT NULL,
    RELJCT1NAME varchar(50)   NOT NULL,
    WRK_ZONENAME varchar(50)   NOT NULL,
    REL_ROADNAME varchar(50)   NOT NULL,
    LGT_CONDNAME varchar(50)   NOT NULL,
    FATALS int   NOT NULL,
	CONSTRAINT us_accident_unique UNIQUE (YEAR_i,ST_CASE)
);

CREATE TABLE us_drug (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    YEAR_i int   NOT NULL,
    VEH_NO int   NOT NULL,
    PER_NO int   NOT NULL,
    DRUGSPEC int   NOT NULL,
    DRUGSPECNAME varchar(50)   NOT NULL,
    DRUGRES int   NOT NULL,
    DRUGRESNAME int   NOT NULL
);

CREATE TABLE us_person (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    YEAR_i int   NOT NULL,
    VE_FORMS int   NOT NULL,
    VEH_NO int   NOT NULL,
    PER_NO int   NOT NULL,
    STR_VEH int   NOT NULL,
    AGE int   NOT NULL,
    AGENAME int   NOT NULL,
    SEX varchar(50)   NOT NULL,
    SEXNAME varchar(50)   NOT NULL,
    PER_TYP int   NOT NULL,
    PER_TYPNAME varchar(50)   NOT NULL,
    INJ_SEV int   NOT NULL,
    INJ_SEVNAME varchar(50)   NOT NULL,
    DRINKING int   NOT NULL,
    DRINKINGNAME varchar(50)   NOT NULL,
    ALC_STATUS int   NOT NULL,
    ALC_STATUSNAME varchar(50)   NOT NULL,
    ATST_TYP int   NOT NULL,
    ATST_TYPNAME varchar(50)   NOT NULL,
    ALC_RES int   NOT NULL,
    ALC_RESNAME varchar(50)   NOT NULL,
    DRUGS int   NOT NULL,
    DRUGSNAME varchar(50)   NOT NULL,
    DSTATUS int   NOT NULL,
    DSTATUSNAME varchar(50)   NOT NULL,
    HISPANIC int   NOT NULL,
    HISPANICNAME varchar(50)   NOT NULL,
	CONSTRAINT us_person_unique UNIQUE (VEH_NO, PER_NO,YEAR_i,ST_CASE) 
);

CREATE TABLE us_vehicle (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    YEAR_i int   NOT NULL,
    VEH_NO int   NOT NULL,
    VE_FORMS int   NOT NULL,
    NUMOCCS int   NOT NULL,
    NUMOCCSNAME int   NOT NULL,
    HIT_RUN int   NOT NULL,
    HIT_RUNNAME varchar(50)   NOT NULL,
    REG_STAT int   NOT NULL,
    REG_STATNAME varchar(50)   NOT NULL,
    BODY_TYP int   NOT NULL,
    BODY_TYPNAME varchar   NOT NULL,
    MOD_YEAR_i int   NOT NULL,
    MOD_YEAR_iNAME int   NOT NULL,
    SPEEDREL int   NOT NULL,
    SPEEDRELNAME varchar(50)   NOT NULL,
    VTRAFWAY int   NOT NULL,
    VTRAFWAYNAME varchar(50)   NOT NULL,
    VNUM_LAN int   NOT NULL,
    VNUM_LANNAME varchar(50)   NOT NULL,
    VSPD_LIM int   NOT NULL,
    VSPD_LIMNAME varchar   NOT NULL,
    VALIGN int   NOT NULL,
    VALIGNNAME varchar(50)   NOT NULL,
    VPROFILE int   NOT NULL,
    VPROFILENAME varchar(50)   NOT NULL,
    VPAVETYP int   NOT NULL,
    DEATHS int   NOT NULL,
    DR_DRINK int   NOT NULL,
    DR_DRINKNAME varchar(50)   NOT NULL,
	CONSTRAINT us_vehicle_unique UNIQUE (VEH_NO,YEAR_i,ST_CASE)
);

CREATE TABLE us_vision (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    YEAR_i int   NOT NULL,
    VEH_NO int   NOT NULL,
    VISION int   NOT NULL,
    VISIONNAME varchar(50)   NOT NULL
);

CREATE TABLE us_race (
    STATE_i int   NOT NULL,
    STATE_iNAME varchar(50)   NOT NULL,
    ST_CASE int   NOT NULL,
    YEAR_i int   NOT NULL,
    VEH_NO int   NOT NULL,
    PER_NO int   NOT NULL,
    RACE int   NOT NULL,
    RACENAME varchar(50)   NOT NULL,
    ORDER_i int   NOT NULL,
    MULTRACE varchar(50)   NOT NULL
	
);


ALTER TABLE us_drug ADD CONSTRAINT fk_us_drug_ST_CASE_YEAR_i_VEH_NO_PER_NO FOREIGN KEY(ST_CASE, YEAR_i, VEH_NO, PER_NO)
REFERENCES us_person (ST_CASE, YEAR_i, VEH_NO, PER_NO);

ALTER TABLE us_person ADD CONSTRAINT fk_us_person_ST_CASE_YEAR_i_VEH_NO FOREIGN KEY(ST_CASE, YEAR_i, VEH_NO)
REFERENCES us_vehicle (ST_CASE, YEAR_i, VEH_NO);

ALTER TABLE us_vehicle ADD CONSTRAINT fk_us_vehicle_ST_CASE_YEAR_i FOREIGN KEY(ST_CASE, YEAR_i)
REFERENCES us_accident (ST_CASE, YEAR_i);

ALTER TABLE us_vision ADD CONSTRAINT fk_us_vision_ST_CASE_YEAR_i_VEH_NO FOREIGN KEY(ST_CASE, YEAR_i, VEH_NO)
REFERENCES us_vehicle (ST_CASE, YEAR_i, VEH_NO);

ALTER TABLE us_race ADD CONSTRAINT fk_us_race_ST_CASE_YEAR_i_VEH_NO_PER_NO FOREIGN KEY(ST_CASE, YEAR_i, VEH_NO, PER_NO)
REFERENCES us_person (ST_CASE, YEAR_i, VEH_NO, PER_NO);
