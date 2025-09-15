from models.insight import Insight
from controllers.insight_controller import InsightController

class insightView:
    def __init__(self):
        self.controller = InsightController()
    def create(self):
        indice = int(input("Indice:"))
        recommendation = input("Recommendation:")
        insight = Insight(indice=indice, recommendation=recommendation)
        self.controller.add(insight=insight)
    def read(self): ...
    def update(self): ...
    def delete(self, id: int): ...
    
    def get_all(self):
        all_insights = self.controller.get_all()

        if all_insights:
            print("\n--- All Insights ---")
            print()
            for insight in all_insights:
                print(f"ID: {insight.id}, Indice: {insight.indice}, Recommendation: {insight.recommendation}")
            print()
        else:
            print("\nNo insights found in the database.")
