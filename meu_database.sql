CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    enrollment_date DATE NOT NULL
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    workload_in_hours INTEGER NOT NULL,
    enrollment_fee DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'paid')),
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_enrollment UNIQUE (student_id, course_id)
);


SELECT
    s.full_name AS student_name,
    SUM(
        CASE WHEN e.status = 'paid' THEN c.enrollment_fee ELSE 0 END
    ) AS total_paid,
    SUM(
        CASE WHEN e.status = 'pending' THEN c.enrollment_fee ELSE 0 END
    ) AS total_due,
    COUNT(*) AS total_enrollments
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id
GROUP BY s.full_name
ORDER BY s.full_name;
