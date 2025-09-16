from models.insight import Insight
from controllers.insight_controller import InsightController

class insightView:
    def __init__(self):
        self.controller = InsightController()
    def create(self):
        indice = int(input("Indice:"))
        recommendation = input("Recommendation:")
        insight = Insight(indice=indice, recommendation=recommendation)
        result, content = self.controller.add(insight=insight)
        if result:
            print("Insight created successfully.")
        else:
            print(f"Error to create a insight: {content}")
    def read(self): ...
    def update(self): ...
    def delete(self, id: int): ...
    
    def get_all(self):
        all_insights, error = self.controller.get_all()

        if error:
            print(f"Error: {error}")
        elif not all_insights:
            print("\nNo insights found in the database.")
        else:
            print("\n--- All Insights ---")
            print()
            for insight in all_insights:
                print(f"ID: {insight.id}, Indice: {insight.indice}, Recommendation: {insight.recommendation}")
            print()

