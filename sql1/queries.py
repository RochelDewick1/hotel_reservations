from sql1 import database_actions 

def get_top_agents_reservations_in_country(country):
    return database_actions.query(
        '''WITH top_agent AS
(       
        SELECT TOP (1)
        r.agent agent, 
        COUNT(r.agent) AS agent_bookings
        FROM Reservation r
        INNER JOIN  guest g 
        ON r.GuestId = g.GuestId
        GROUP BY r.agent, g.country
        HAVING   g.country = \'''' + country + 
        '''\' ORDER BY agent_bookings DESC)

        SELECT TOP (10)
        r.*, g.*
        FROM top_agent
        LEFT JOIN RESERVATION r ON top_agent.agent = r.agent
        LEFT JOIN Guest g ON r.GuestId = g.GuestId
        WHERE g.country = \''''+ country + '''\' ;'''
    )

def get_info_for_yr_within_adr(year, ADR1, ADR2):
   return database_actions.query(
    '''SELECT *
    FROM Reservation r
    INNER JOIN Guest g ON g.GuestId = r.GuestId
    WHERE YEAR(r.arrival_date) = ''' +str(year) +'''
    AND (r.adr BETWEEN ''' + str(ADR1) +''' AND ''' + str(ADR2) +''')
    AND (r.is_canceled != 1);'''   
   ) 

def show_num_children_impacts_nights():
    return database_actions.query(
       '''SELECT AVG(r.stays_in_weekend_nights+ r.stays_in_week_nights) nights,
        g.children children
       FROM Guest g
       INNER JOIN Reservation r ON g.GuestId = R.GuestId
       GROUP BY children
       ORDER BY children;''')

def average_adr_per_country():
    return database_actions.query(
        '''SELECT g.country country,
	   AVG(r.ADR) avg_rate
    FROM Guest g
    INNER JOIN Reservation r ON g.GuestId = R.GuestId
    GROUP BY country
    ORDER BY avg_rate;''') 
