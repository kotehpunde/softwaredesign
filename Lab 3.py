#Question 1
def calculate_volume_pyramid_or_cone(base_area, height):
    volume = (1/3)*base_area*height
    return volume

def main():
    shape = input("Enter a shape (Pyramid or Cone): ").lower()

    if shape == "pyramid" or shape == "cone":
        base_area = float(input("Enter a base area: "))
        height = float(input("Enter a height: "))
        volume = calculate_volume_pyramid_or_cone(base_area, height)
        print("The volume of the", shape, "is", round(volume, 2))
    else:
        print ("Invalid shape")

if __name__ == "__main__":
    main()
'''
line 17 and 18 is liddat to let python know that we want to run the main() first!!!
if not it will run line 1,2,3 first 
'''
print("---------------------------------------------------------------")

#Question 2
import math
def calculate_volume_of_sphere(radius):
    volume = (4/3)*math.pi*(radius**3)
    return volume

def main():
    radius = float(input("Enter a radius: "))
    volume = calculate_volume_of_sphere(radius)
    print("The volume of the sphere is:", round(volume, 2))

if __name__ == "__main__":
    main()
print("----------------------------------------------------------------")

#Question 3
def multiply(num1, num2):
    times = num1*num2
    return times

def main():
    num1 = float(input("Enter a number: "))
    num2 = float(input("Enter another number: "))
    times = multiply(num1, num2)
    print("The answer is:", "{:.2f}".format(times))

if __name__ == "__main__":
    main()
print("---------------------------------------------------------------")

#Question 4
def length_of_square(length):
    perimeter = 4*length
    return perimeter

def main():
    length = float(input("Enter a length:"))
    perimeter = length_of_square(length)
    print("The perimeter of a square is:", "{:.2f}".format(perimeter))

if __name__ == "__main__":
    main()
print("---------------------------------------------------------------")

#Question 5
def perimeter_of_rectangle(length, width):
    perimeter = (2*length) + (2*width)
    return perimeter

def main():
    length = float(input("Enter length: "))
    width = float(input("Enter width: "))
    perimeter = perimeter_of_rectangle(length, width)
    print("Perimeter of rectangle is: ", "{:.2f}".format(perimeter))

if __name__ == "__main__":
    main()
print("--------------------------------------------------------------")

#Question 6
import math
def radius_of_circle(radius):
    area_of_circle = math.pi*(radius**2)
    return area_of_circle

def main():
    radius = float(input("Enter radius of circle: "))
    area_of_circle = radius_of_circle(radius)
    print("Area of circle is: ", "{:.2f}".format(area_of_circle))

if __name__ == "__main__":
    main()
print("-------------------------------------------------------------")

#Question 7
import math
def radius_height_of_cylinder(radius, height):
    volume = math.pi*(radius**2)*height
    return volume

def main():
    radius = float(input("Enter a radius: "))
    height = float(input("Enter a height: "))
    volume = radius_height_of_cylinder(radius, height)
    print("Volume of cylinder is: ", "{:.2f}".format(volume))

if __name__ == "__main__":
    main()
print("-----------------------------------------------------------")

#Question 8
import math
def radius_height_of_cylinder(radius, height):
    area_of_cylinder = (2*math.pi*radius*height) + (2*math.pi*(radius**2))
    return area_of_cylinder

def main():
    radius = float(input("Enter a radius: "))
    height = float(input("Enter a height: "))
    area = radius_height_of_cylinder(radius, height)
    print("The area of the cylinder is: ", "{:.2f}".format(area))

if __name__ == "__main__":
    main()