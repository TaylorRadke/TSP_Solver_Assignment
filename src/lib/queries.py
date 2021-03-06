sql_add_solution = """
    INSERT INTO Solution
    (ProblemName,TourLength,Date,Author,Algorithm,RunningTime,Tour)
    Values
    ('{name}',{length},CURDATE(),'Taylor','Greedy 2-opt',{runningtime},'{tour}');
    """

sql_get_cities = """
    SELECT ID,x,y from Cities
    WHERE Name = '{name}';
    """ 

sql_add_city = """
    INSERT INTO Cities (Name,ID,x,y)
    Values
    ('{name}',{id},{x},{y});
    """

sql_get_tour_length = """
    SELECT TourLength
    FROM Solution
    WHERE ProblemName = '{name}'
    LIMIT 1;
    """

sql_add_problem = """
    INSERT INTO Problem (Name,Size,Comment)
    Values
    ('{name}',{size},'{comment}'); 
    """

sql_get_problems ="""
    SELECT *
    FROM Problem
    """

sql_get_solutions ="""
    SELECT ProblemName
    FROM Solution
    LIMIT 1;
    """
sql_get_solution_times ="""
    SELECT RunningTime
    FROM Solution
    WHERE ProblemName = '{name}';
    """

sql_get_solution_cities = """
    SELECT Tour
    FROM Solution
    WHERE ProblemName = '{name}'
    AND RunningTime = {runningtime}
    LIMIT 1;
    """
sql_get_city = """
    SELECT ID,x,y
    FROM Cities
    WHERE Name = '{name}'
    AND ID = {id}
    LIMIT 1;
    """