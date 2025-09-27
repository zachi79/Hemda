SELECT current_database();

CREATE TABLE IF NOT EXISTS teachers (
    user_id SERIAL PRIMARY KEY,
    teacherName VARCHAR(255),
    phone VARCHAR(50),
    profession VARCHAR(50),
	email VARCHAR(100),
	color VARCHAR(50)
);


INSERT INTO teachers (teacherName, phone, profession, email, color) VALUES
('אדי יוסוב', '054-5896321', 'פיסיקה', '#FF5733'), -- Coral
('אודין קלס', '054-3214567', 'פיסיקה', '#FFBD33'), -- Tangerine
('אורי איגר', '054-9876543', 'פיסיקה', '#F2FF33'), -- Bright Yellow
('אורן פרבר', '054-1239874', 'פיסיקה', '#99FF33'), -- Neon Green
('איל כהן', '054-7894561', 'פיסיקה', '#33FFBD'), -- Aqua
('אלון מוסקונה', '054-6547893', 'פיסיקה', '#33E6FF'), -- Sky Blue
('אלונה ורד', '054-1597538', 'פיסיקה', '#3399FF'), -- Dodger Blue
('אריאלה זגל', '054-8529631', 'פיסיקה', '#334DFF'), -- Royal Blue
('אריק גלבוע', '054-7418529', 'פיסיקה', '#7733FF'), -- Lavender
('אריק רוזנברג', '054-3692587', 'פיסיקה', '#BD33FF'), -- Purple
('גלעד סבירסקי', '054-8975641', 'פיסיקה', '#E633FF'), -- Magenta
('חיים שמואלי', '054-1472583', 'פיסיקה', '#FF33E6'), -- Hot Pink
('טל וייס', '054-7539518', 'פיסיקה', '#FF3399'), -- Deep Pink
('יבגני ברודצקי', '054-9638521', 'פיסיקה', '#FF334D'), -- Crimson
('ילנה סימון', '054-1234567', 'פיסיקה', '#FF6666'), -- Salmon
('יפתח אילסר', '054-9876543', 'פיסיקה', '#FF9966'), -- Apricot
('ליאור יוסוב', '054-4567891', 'פיסיקה', '#FFCC66'), -- Gold
('מיכאל לוי', '054-1235789', 'פיסיקה', '#FFFF66'), -- Lemon
('מתיאס בירמן', '054-8796541', 'פיסיקה', '#CCFF66'), -- Lime Green
('נועם איל', '054-3571598', 'פיסיקה', '#99FF66'), -- Spring Green
('נועם דוד', '054-7412589', 'פיסיקה', '#66FF99'), -- Emerald
('נועם ליאור', '054-8523697', 'פיסיקה', '#66FFCC'), -- Teal
('סלימאן אבו טאלב', '054-1596328', 'פיסיקה', '#66FFFF'), -- Cyan
('עדי זומר', '054-7531598', 'פיסיקה', '#66CCFF'), -- Light Blue
('עידית גרומן', '054-9517532', 'פיסיקה', '#6699FF'), -- Sky Blue
('עמית חן', '054-8521479', 'פיסיקה', '#6666FF'), -- Periwinkle
('עמר ליכטנשטיין', '054-6547893', 'פיסיקה', '#9966FF'), -- Grape
('ראובן שפיטלניק', '054-9871236', 'פיסיקה', '#CC66FF'), -- Violet
('שי נוטר', '054-7894563', 'פיסיקה', '#FF66FF'), -- Fuchsia
('שלמה רוזנפלד', '054-2583691', 'פיסיקה', '#FF66CC'), -- Orchid
('אביב חגולי', '054-8521473', 'כימיה', '#FF6699'), -- Rose
('אושרית פוליקר', '054-7418523', 'כימיה', '#FF9999'), -- Light Salmon
('אירנה אסייג', '054-9638527', 'כימיה', '#FFCCCC'), -- Pale Pink
('איתן קריין', '054-1592584', 'כימיה', '#FFB2B2'), -- Blush
('אסנת רווה', '054-7538965', 'כימיה', '#FF99CC'), -- Hot Pink
('בן אושר', '054-8523697', 'כימיה', '#FFB2E6'), -- Light Magenta
('דינה דנה', '054-1597532', 'כימיה', '#E6B2FF'), -- Light Purple
('זאב זיניוק', '054-3698521', 'כימיה', '#B2B2FF'), -- Light Periwinkle
('יוליה ויינר', '054-7415829', 'כימיה', '#B2E6FF'), -- Light Sky Blue
('יעל הרץ', '054-9638521', 'כימיה', '#B2FFD8'), -- Light Turquoise
('מריה זצפין', '054-1236547', 'כימיה', '#D8FFB2'), -- Light Lime Green
('נטלי הולצמן', '054-8974561', 'כימיה', '#E6FFB2'), -- Pale Green
('רון שוורץ', '054-1597532', 'כימיה', '#FFD8B2'), -- Light Orange
('רעיה קוברסקי', '054-9638521', 'כימיה', '#FFB2D8'); -- Muted Pink


INSERT INTO teachers (teacherName, phone, profession, email, color) VALUES
('אדי יוסוב', '054-5896321', 'פיסיקה', 'adi.yosuv@physics.com', '#FF5733'),
('אודין קלס', '054-3214567', 'פיסיקה', 'odin.kles@physics.com', '#FFBD33'),
('אורי איגר', '054-9876543', 'פיסיקה', 'uri.iger@physics.com', '#F2FF33'),
('אורן פרבר', '054-1239874', 'פיסיקה', 'oren.farber@physics.com', '#99FF33'),
('איל כהן', '054-7894561', 'פיסיקה', 'eyal.cohen@physics.com', '#33FFBD'),
('אלון מוסקונה', '054-6547893', 'פיסיקה', 'alon.moskona@physics.com', '#33E6FF'),
('אלונה ורד', '054-1597538', 'פיסיקה', 'alona.vered@physics.com', '#3399FF'),
('אריאלה זגל', '054-8529631', 'פיסיקה', 'ariela.zagal@physics.com', '#334DFF'),
('אריק גלבוע', '054-7418529', 'פיסיקה', 'arik.gilboa@physics.com', '#7733FF'),
('אריק רוזנברג', '054-3692587', 'פיסיקה', 'arik.rosenberg@physics.com', '#BD33FF'),
('גלעד סבירסקי', '054-8975641', 'פיסיקה', 'gilad.svirsky@physics.com', '#E633FF'),
('חיים שמואלי', '054-1472583', 'פיסיקה', 'chaim.shmueli@physics.com', '#FF33E6'),
('טל וייס', '054-7539518', 'פיסיקה', 'tal.weiss@physics.com', '#FF3399'),
('יבגני ברודצקי', '054-9638521', 'פיסיקה', 'yevgeny.brodetsky@physics.com', '#FF334D'),
('ילנה סימון', '054-1234567', 'פיסיקה', 'yelena.simon@physics.com', '#FF6666'),
('יפתח אילסר', '054-9876543', 'פיסיקה', 'yiftach.eyser@physics.com', '#FF9966'),
('ליאור יוסוב', '054-4567891', 'פיסיקה', 'lior.yosuv@physics.com', '#FFCC66'),
('מיכאל לוי', '054-1235789', 'פיסיקה', 'michael.levy@physics.com', '#FFFF66'),
('מתיאס בירמן', '054-8796541', 'פיסיקה', 'matias.birman@physics.com', '#CCFF66'),
('נועם איל', '054-3571598', 'פיסיקה', 'noam.ayal@physics.com', '#99FF66'),
('נועם דוד', '054-7412589', 'פיסיקה', 'noam.david@physics.com', '#66FF99'),
('נועם ליאור', '054-8523697', 'פיסיקה', 'noam.lior@physics.com', '#66FFCC'),
('סלימאן אבו טאלב', '054-1596328', 'פיסיקה', 'sulaiman.abu.taleb@physics.com', '#66FFFF'),
('עדי זומר', '054-7531598', 'פיסיקה', 'adi.zomer@physics.com', '#66CCFF'),
('עידית גרומן', '054-9517532', 'פיסיקה', 'idit.groman@physics.com', '#6699FF'),
('עמית חן', '054-8521479', 'פיסיקה', 'amit.chen@physics.com', '#6666FF'),
('עמר ליכטנשטיין', '054-6547893', 'פיסיקה', 'omer.lichtenstein@physics.com', '#9966FF'),
('ראובן שפיטלניק', '054-9871236', 'פיסיקה', 'reuven.shpitalnik@physics.com', '#CC66FF'),
('שי נוטר', '054-7894563', 'פיסיקה', 'shai.nuter@physics.com', '#FF66FF'),
('שלמה רוזנפלד', '054-2583691', 'פיסיקה', 'shlomo.rosenfeld@physics.com', '#FF66CC'),
('אביב חגולי', '054-8521473', 'כימיה', 'aviv.chaguli@chemistry.com', '#FF6699'),
('אושרית פוליקר', '054-7418523', 'כימיה', 'ushrit.poliker@chemistry.com', '#FF9999'),
('אירנה אסייג', '054-9638527', 'כימיה', 'irena.asyag@chemistry.com', '#FFCCCC'),
('איתן קריין', '054-1592584', 'כימיה', 'eitan.krein@chemistry.com', '#FFB2B2'),
('אסנת רווה', '054-7538965', 'כימיה', 'osnat.rave@chemistry.com', '#FF99CC'),
('בן אושר', '054-8523697', 'כימיה', 'ben.osher@chemistry.com', '#FFB2E6'),
('דינה דנה', '054-1597532', 'כימיה', 'dina.dana@chemistry.com', '#E6B2FF'),
('זאב זיניוק', '054-3698521', 'כימיה', 'zeev.ziniuk@chemistry.com', '#B2B2FF'),
('יוליה ויינר', '054-7415829', 'כימיה', 'yulia.veiner@chemistry.com', '#B2E6FF'),
('יעל הרץ', '054-9638521', 'כימיה', 'yael.hertz@chemistry.com', '#B2FFD8'),
('מריה זצפין', '054-1236547', 'כימיה', 'maria.zatspin@chemistry.com', '#D8FFB2'),
('נטלי הולצמן', '054-8974561', 'כימיה', 'natali.holtzman@chemistry.com', '#E6FFB2'),
('רון שוורץ', '054-1597532', 'כימיה', 'ron.shvartz@chemistry.com', '#FFD8B2'),
('רעיה קוברסקי', '054-9638521', 'כימיה', 'raya.kobersky@chemistry.com', '#FFB2D8');


CREATE TABLE IF NOT EXISTS rooms (
    roomNumber VARCHAR(50) PRIMARY KEY,
    profession VARCHAR(50) DEFAULT 'כללי'
);

INSERT INTO rooms (roomNumber) VALUES
('102'),('103'),('104'),('105'),('106'),('107'),
('202'),('203'),('204'),('205'),('206'),('207'),
('302'),('303'),('304'),('305'),('306'),('307'),
('402'),('403'),('404'),('405'),('406'),('407'),
('חדר ישיבות'),('ספריה'),('אודיטוריום');


CREATE TABLE IF NOT EXISTS schools (
    schoolName VARCHAR(255) PRIMARY KEY,
    schoolPhone VARCHAR(50),
    schoolLocation VARCHAR(255)
);


INSERT INTO schools (schoolName, schoolPhone, schoolLocation) VALUES
	('אג''יאל', '03-6888888', 'דרך ירושלים 66, יפו'),
    ('אולפנית', '03-5188888', 'רחוב הרצל 106, תל אביב-יפו'),
    ('אליאנס', '03-6966666', 'רחוב צייטלין 1, תל אביב-יפו'),
    ('בר אילן', '03-6055555', 'רחוב בן יהודה 94, תל אביב-יפו'),
    ('גורדון', '03-6955555', 'רחוב גורדון 59, תל אביב-יפו'),
    ('גע"ה', '03-5177777', 'רחוב שדרות ירושלים 136, תל אביב-יפו'),
    ('ד.פ.', '03-6044444', 'רחוב דפנה 5, תל אביב-יפו'),
    ('יאפא אלמ''', '03-6822222', 'דרך ירושלים 122, יפו'),
    ('יצחק שמיר', '03-6055555', 'רחוב אליפלט 4, תל אביב-יפו'),
    ('ליידי דיוויס', '03-5288888', 'רחוב שינקין 2, תל אביב-יפו'),
    ('סטודיו אנקורי', '03-6444444', 'רחוב שמעון התרסי 18, תל אביב-יפו'),
    ('סינג', '03-6988888', 'רחוב צייטלין 2, תל אביב-יפו'),
    ('ע. א', '03-5244444', 'רחוב חיים לבנון 12, תל אביב-יפו'),
    ('ע. ב''ג', '03-5222222', 'רחוב שדרות בן גוריון 14, תל אביב-יפו'),
    ('ע. ה', '03-6955555', 'רחוב האלה 3, תל אביב-יפו'),
    ('ע. ו', '03-5222222', 'רחוב וולפסון 18, תל אביב-יפו'),
    ('ע. ז', '03-6955555', 'רחוב זבוטינסקי 7, תל אביב-יפו'),
    ('ע. ט', '03-5222222', 'רחוב טשרניחובסקי 3, תל אביב-יפו'),
    ('ע. י''ד', '03-6955555', 'רחוב י''ד 10, תל אביב-יפו'),
    ('ע. י''ב', '03-5222222', 'רחוב י''ב 5, תל אביב-יפו'),
    ('עמוס עוז', '03-6888888', 'רחוב עזרא 12, תל אביב-יפו'),
    ('פלך', '03-6966666', 'רחוב פלך 15, תל אביב-יפו'),
    ('צמרות', '03-6955555', 'רחוב צמרות 20, תל אביב-יפו'),
    ('ראשית בנות', '03-6888888', 'רחוב ראשית 5, תל אביב-יפו'),
    ('רוגוזין', '03-6966666', 'רחוב רוגוזין 10, תל אביב-יפו'),
    ('תיכון חדש', '03-5255555', 'רחוב משה שרת 1, תל אביב-יפו'),
    ('תיכונט', '03-6444444', 'רחוב ש"י עגנון 20, תל אביב-יפו');


CREATE TABLE IF NOT EXISTS timeTable (
    schoolName VARCHAR(255) PRIMARY KEY,
    schoolPhone VARCHAR(50),
    schoolLocation VARCHAR(255)
);



CREATE TABLE fixed_timetable (
    day_of_week VARCHAR(15) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    yearSelect VARCHAR(50) NOT NULL,
    teacher_name VARCHAR(50) NOT NULL,
    profession VARCHAR(50) NOT NULL,
    schoolName VARCHAR(255) NOT NULL,
    schoolClass VARCHAR(255) NOT NULL,
    room_number VARCHAR(10) NOT NULL
);


CREATE TABLE dynamic_timetable (
    day_of_week VARCHAR(15) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
	yearSelect VARCHAR(50) NOT NULL,
	weekSelect VARCHAR(50) NOT NULL,
    teacher_name VARCHAR(50) NOT NULL,
    profession VARCHAR(50) NOT NULL,
	schoolName VARCHAR(255) NOT NULL,
	schoolClass VARCHAR(255) NOT NULL,
    room_number VARCHAR(10) NOT NULL	
);



CREATE TABLE testsBoard (
	schoolName VARCHAR(255) NOT NULL,
	schoolClass VARCHAR(255) NOT NULL,	
	teacher_name VARCHAR(50) NOT NULL,
    profession VARCHAR(50) NOT NULL,
	room_number VARCHAR(10) NOT NULL,
	Test1 Date,
	Test2 Date,
	Test3 Date,
	Test4 Date,
	Test5 Date,
	Test6 Date,
	matkonetTest Date,
	LabTest Date
);


CREATE TABLE testsBoard (
	schoolName VARCHAR(255) NOT NULL,
	schoolClass VARCHAR(255) NOT NULL,	
	teacher_name VARCHAR(50) NOT NULL,
    profession VARCHAR(50) NOT NULL,
	room_number VARCHAR(10) NOT NULL,
	Test1 VARCHAR(50),
	Test2 VARCHAR(50),
	Test3 VARCHAR(50),
	Test4 VARCHAR(50),
	Test5 VARCHAR(50),
	Test6 VARCHAR(50),
	matkonetTest VARCHAR(50),
	LabTest VARCHAR(50)
);


INSERT INTO public.testsboard(
	schoolname, schoolclass, teacher_name, profession, room_number, test1, test2, test3, test4, test5, test6, matkonettest, labtest)
	VALUES ('אליאנס',
	'י1', 
	'נטליה הולצמן',
	'כימיה',
	'107', 
	'2025-11-27', 
	NULL, 
	NULL, 
	NULL, 
	NULL, 
	NULL, 
	NULL, 
	NULL);
