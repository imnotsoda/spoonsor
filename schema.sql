-- =============================================
-- CS348 Project: Campus Fundraising Deals App
-- =============================================

DROP TABLE IF EXISTS Deals;
DROP TABLE IF EXISTS Organizations;
DROP TABLE IF EXISTS Restaurants;

-- =============================================
-- TABLE DEFINITIONS
-- =============================================

CREATE TABLE Organizations (
    org_id        SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    description   TEXT,
    contact_email VARCHAR(100)
);

CREATE TABLE Restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    location      VARCHAR(200),
    category      VARCHAR(50),
    lat           NUMERIC(9,6),
    lng           NUMERIC(9,6)
);

CREATE TABLE Deals (
    deal_id          SERIAL PRIMARY KEY,
    org_id           INT NOT NULL REFERENCES Organizations(org_id) ON DELETE CASCADE,
    restaurant_id    INT NOT NULL REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE,
    promo_code       VARCHAR(50)   NOT NULL,
    donation_percent NUMERIC(5,2) NOT NULL,
    start_date       DATE         NOT NULL,
    end_date         DATE         NOT NULL,
    is_active        BOOLEAN      DEFAULT TRUE,
    note             TEXT,
    instruction      TEXT,
    poster_url       VARCHAR(500)
);

-- =============================================
-- SAMPLE DATA
-- =============================================

INSERT INTO Organizations (name, description, contact_email) VALUES
    ('Purdue CS Club',        'Computer science students building cool things.',            'csclub@purdue.edu'),
    ('Purdue Dance Marathon',  'Annual fundraiser supporting Riley Hospital for Children.', 'pdm@purdue.edu'),
    ('Boilermaker Robotics',  'Competitive robotics team representing Purdue.',             'robotics@purdue.edu'),
    ('Pre-Med Society',       'Supporting students pursuing careers in medicine.',          'premed@purdue.edu'),
    ('Purdue Sustainability',  'Promoting eco-friendly initiatives on campus.',             'sustain@purdue.edu');

INSERT INTO Restaurants (name, location, category, lat, lng) VALUES
    ('Pizza Uncommon',             '111 S Salisbury St Suite 120, West Lafayette, IN', 'Sit-down',  40.422562, -86.905781),
    ('Tsaocaa',                    '318 W State St, West Lafayette, IN',               'Cafe',      40.424068, -86.908807),
    ('HotBox Pizza',               '302 Vine St Ste 120, West Lafayette, IN',          'Fast Food', 40.426055, -86.907897),
    ('Chipotle',                   '200 W State St, West Lafayette, IN',               'Fast Food', 40.423630, -86.907157),
    ('Raising Cane''s',            '100 S Chauncey Ave Ste 100, West Lafayette, IN',   'Fast Food', 40.422886, -86.906542),
    ('Vienna Espresso Bar & Bakery','208 South St, West Lafayette, IN',                'Cafe',      40.424033, -86.907567);

INSERT INTO Deals (org_id, restaurant_id, promo_code, donation_percent, start_date, end_date, is_active, note, instruction, poster_url) VALUES
    (1, 1, 'CSUNCOMMON',  12.00, '2026-03-01', '2026-04-30', TRUE,
        'Valid on all pizzas. Dine-in and carry-out.',
        'Tell your server "CS Club fundraiser" before placing your order.',
        NULL),

    (1, 2, 'CSBOBA15',    15.00, '2026-03-15', '2026-05-15', TRUE,
        'Valid on all drinks and waffles.',
        'Mention the promo code on the touchscreen or to the cashier.',
        NULL),

    (2, 4, 'PDM20',       20.00, '2026-02-01', '2026-03-31', FALSE,
        'Valid on all entrees. Excludes drinks and chips.',
        'Show your PDM fundraiser flyer at the register.',
        NULL),

    (2, 3, 'PDMHOTBOX',   12.00, '2026-04-01', '2026-04-30', TRUE,
        'Valid on any pizza. No minimum order.',
        'Enter "PDM" in the order name field when ordering online or in-store.',
        NULL),

    (3, 5, 'ROBOTS15',    15.00, '2026-03-20', '2026-04-20', TRUE,
        'Valid on combo meals only.',
        'Say "Boilermaker Robotics" when placing your order.',
        NULL),

    (4, 6, 'PREMED10',    10.00, '2026-03-01', '2026-05-01', TRUE,
        'Valid on all drinks and food items.',
        'Mention the Pre-Med Society fundraiser to the barista before paying.',
        NULL),

    (5, 2, 'GREENBOBA',   12.00, '2026-04-01', '2026-04-22', TRUE,
        'Earth Day special — valid on all drinks.',
        'Show the Purdue Sustainability Instagram post at the counter.',
        NULL),

    (3, 4, 'BOTCHIPOTLE', 18.00, '2026-01-01', '2026-02-28', FALSE,
        'Valid on burrito bowls and burritos only.',
        'Tell the cashier "Boilermaker Robotics" before they ring you up.',
        NULL);


-- =============================================
-- INDEXES
-- =============================================
CREATE INDEX idx_deals_org_id ON Deals(org_id);
CREATE INDEX idx_deals_restaurant_id ON Deals(restaurant_id);
CREATE INDEX idx_deals_is_active ON Deals(is_active);
CREATE INDEX idx_restaurants_category ON Restaurants(category);