
from django.contrib import admin
from .models import Student, Attendance, Class

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id')
    search_fields = ('name', 'student_id')
    list_filter = ('classes',)
    ordering = ('name',) 
    actions = ['activate_students', 'deactivate_students']   # Custom bulk actions for the students


    def get_classes(self, obj):
        print(obj.classes.all())
        return ", ".join([c.name for c in obj.classes.all()])
    get_classes.short_description = 'Classes'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student','get_class', 'date', 'status')
    list_filter = ('status', 'date', 'student__classes')  # Filter by class and status
    search_fields = ('student__name', 'date')  # Search by student name and date
    ordering = ('-date',) #default ordering by date in descending order
    actions = ['mark_present', 'mark_absent']


    def mark_present(self, request, queryset):
        queryset.update(status='Present')
        self.message_user(request, "Selected attendance records marked as Present.")

    def mark_absent(self, request, queryset):
        queryset.update(status='Absent')
        self.message_user(request, "Selected attendance records marked as Absent.")


    def get_class(self,obj):
        classes=obj.student.classes.all()
        class_name=[c.name for c in classes]
        return ", ".join(class_name)
      
    get_class.short_description = 'Class'
    mark_present.short_description = 'Mark selected as Present'
    mark_absent.short_description = 'Mark selected as Absent'



class StudentInline(admin.TabularInline):
    model = Class.students.through  # Many-to-Many relationship with Class
    extra = 1  # Number of extra forms shown by default

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):


    list_display = ('name', 'get_students')
    search_fields = ('name',)  # Search by class name
    inlines = [StudentInline]  # Inline editing for students
    filter_horizontal = ('students',)  #  multi-selection of students
    actions = ['assign_random_students']  # Custom action
    def get_students(self, obj):
        return ", ".join([s.name for s in obj.students.all()])