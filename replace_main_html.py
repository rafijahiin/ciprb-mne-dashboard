with open('dashboard/templates/dashboard/main.html', 'r') as f:
    content = f.read()

new_sections = """<!-- Lagging Behind Districts Section -->
        <div class="bg-gray-800 p-6 rounded-xl shadow-md border border-gray-700 mb-8">
            <h2 class="text-xl font-bold mb-4 text-rose-500">{% trans "Lagging Behind Districts" %}</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-700 text-gray-300">
                            <th class="p-3 border-b border-gray-600">District</th>
                            <th class="p-3 border-b border-gray-600">Pending/Stalled Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for district in lagging_districts %}
                        <tr class="border-b border-gray-700 hover:bg-gray-750">
                            <td class="p-3 text-sm">{{ district.district }}</td>
                            <td class="p-3 text-sm font-bold text-rose-400">{{ district.lagging_count }}</td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="2" class="p-4 text-center text-gray-500">No lagging districts found.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Routine Day-to-Day Activities -->
        <div class="bg-gray-800 p-6 rounded-xl shadow-md border border-gray-700 mb-8">
            <h2 class="text-xl font-bold mb-4 text-emerald-500">{% trans "Recent Day-to-Day Activities" %}</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-700 text-gray-300">
                            <th class="p-3 border-b border-gray-600">Partner</th>
                            <th class="p-3 border-b border-gray-600">Activity</th>
                            <th class="p-3 border-b border-gray-600">Staff</th>
                            <th class="p-3 border-b border-gray-600">Beneficiaries</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for activity in recent_activities %}
                        <tr class="border-b border-gray-700 hover:bg-gray-750">
                            <td class="p-3 text-sm">{{ activity.get_partner_display }}</td>
                            <td class="p-3 text-sm">{{ activity.activity_type }}</td>
                            <td class="p-3 text-sm">{{ activity.staff_name }}</td>
                            <td class="p-3 text-sm">{{ activity.beneficiary_count }}</td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="4" class="p-4 text-center text-gray-500">No recent activities logged.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Bottom Section: MPDSR Event Table with HTMX -->"""

content = content.replace('<!-- Bottom Section: MPDSR Event Table with HTMX -->', new_sections)

with open('dashboard/templates/dashboard/main.html', 'w') as f:
    f.write(content)
