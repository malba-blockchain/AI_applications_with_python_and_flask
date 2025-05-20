def area_of_rectangle(length, breadth):
    """
    This function returns the area of a rectangle
    
    Args:
        length: The length of the rectangle
        breadth: The breadth of the rectangle
        
    Returns:
        The area of the rectangle (length * breadth)
    """
    return length * breadth

def area_of_circle(radius):
    """
    This function returns the area of a circle
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle (π * radius^2)
    """
    import math
    return math.pi * (radius ** 2)