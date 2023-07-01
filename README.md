# T2A2 Mcbroken
***

## Installation Instructions


***

## R1 + R2 Identification of the problem you are trying to solve by building this particular app and why is it a problem that needs solving?

The problem that I am trying to solve with this simple API is to create a way that peolpe are able to communicate when an ice cream machine is broken at Mcdonalds.  This is a problem that needs solving because the problem of ice cream machines being broken at a Mcdonalds has been so prevalent that it has become a running joke that they never work. By creating this community based reporting system it would be something that can 

The problem that is trying to be solved with the creation of the app that uses commnunity reports on broken Mcdonald's ice cream machines is the annoyance and frustration that customers have when they find out the ice cream machine is broken. This problem has become so prevalent that it has become a running joke that they never work.

Reasons for this to be solved;
1. Customer Resolution: Customers come to Mcdonald's wanting soft serves, and Mcflurries however because of the above issue it's become a running joke that they are always up in the air whether they are able to get them or not. This causes dissatisfaction and disappointment among customers, though I am making this for community in mind with comments and upvotes rather than Mcdonald's itself, though it would be something Mcdonalds could add to their app.
2. Time and Effort: Following from the previous point, people knowing in advance whether or not the machine is broken would save them time, money and effort. With the app users would be able to check the status of nearby Mcdonald's locations and decide which one to visit making sure they go with ones that have the most recent reports of operational.
3. Machine Fixing: Although I would want this to be for community in mind, if Mcdonald's did do something along these lines it would help with reporting problems with machines and hopefully fixing them. A future solution could also include data analysis for machines breaking down and when for maintenance and reducing machine downtime as well as making it more efficient for Mcdonald's.
4. Accountability: With a global brand such as Mcdonald's it may be quite difficult to maintain and check every issue their machines have, however with the app it allows the users around the world to have control and hold Mcdonald's accountable for this problem in particular.

***

## R3 Why have you chosen this database system. What are the drawbacks compared to others?

For this database system I have chosen to use Postgres. The reason for this is because it is a relation database, which is suited for an app such as this one that requires data to have structured relationships such as broker ice cream machines and their infomration that we will be using such as location, user report, time, etc. This can be done through the ability to define tables, establish the relationships between them and create queries that are efficient using PostgreSQL. Data integrity is also a key point for this as it ensures that data stored in the database is consistent and accurate which is important for making sure that the information on broken machine reports is correct and up to date with any changes being constantly made and upvoted by users.

In future if this was to be developed further for other purposes or even as the Mcdonald's brand as a whole as it is a global brand with over 38.000 locations across the world Postgres is known for its scaling ability to handle a large dataset and process queries efficiently as long as it's setup correctly. As the app grows over time and users, data, and possibly other information it will be able to handle the data and ensure a smooth performance for the API. This particularly will be very important for handling community reports which can come in and be updated quickly for real time updates on machine status. Thinking of the future as well since it is a well known and used database system the support system that it has for features, extensions and communities are quite large which means that there are a lot of ways the app could grow and be used. An example of this is the ability to provide geospatial data which can be used for mapping and locating Mcdonald's restaurants with working machines.

PLACEHOLDER FOR IMAGE OF DATABASE 

[What is PSQL -AWS](https://aws.amazon.com/rds/postgresql/what-is-postgresql/)

[Why PSQL](https://fulcrum.rocks/blog/why-use-postgresql-database)

Coder Academy Slides and Notes

***

## R4 Identify and discuss the key functionalities and benefits of an ORM

An ORM or Object Relational Mapping is a technique or tool in in software development that helps developers interact with databases. When interacting with a database using languages (OOP), CRUD operations are completed to do this, normally this requires the use of SQL, this is made simpler by using an ORM. It is similar to a layer in that it translates the data between what is used in the databases and the language used in the OOP implementation. In general they are used as an abstraction technique to increase productivity by removing need for boilerplate code and avoid use of awkward techniques to bypass any laguange parameters.

An example of this is below where code is made shorter and simpler using an ORM tool:

```
# From freeCodeCamp
SELECT id, name, email, country, phone_number FROM users WHERE id = 20
# Changed to below
users.GetById(20)
```

By doing this and mapping the databases to object classes in the OOP language a developer can work with something that they are familiar with such as objects, inheritance and encapsulation, this would  make the code simpler and increase productivity as it's something they already know it is easier to maintain and create. ORM's also tend to have other similarities to OOPs such as inheritance and encapsulation. Furthermore because of ORM's and their layer of abstraction provided it allows a developer to use different database systems without making significant changes to the code to be usable. 

In the Mcbroken app I will be using the tool SQLAlchemy which has the structures available to be seen below.

TABLE IN PSQL:

SQLAlchemy MODEL:

GET REQUEST:


[What is an ORM](https://www.prisma.io/dataguide/types/relational/what-is-an-orm)

[What is an ORM freeCodeCamp](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/)

Coder Academy Notes and Slides

***
## R5 Document all endpoints for your API

Example payload to report a machine
{
  "broken": true,
  "location": {
    "number": "123",
    "street": "Main Street",
    "postcode": "12345",
    "suburb": "Example Suburb",
    "state": "Example State"
  }
}

## R10 Describe the way tasks are allocated and tracked in your project

Day 1 
1. Kanban Board
2. Trying to figure out where to start with the coding portion
3. ERD Models 
4. Learned Notions new Project and Tasks model

Day 2 
1. ERD Models thought out
2. Unsure as of yet
3. ERD Diagram and Questions R1-R4
4. Planning using new model from Notion is way easier

Day 3
1. Finished R1-R4
2. Trying to figure out the correct relationships in model
3. ERD Diagram and ERD questions
4. NA