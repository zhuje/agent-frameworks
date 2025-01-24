# Draft Documentation: Logging the Steps Taken  

The **Bee Framework** provides two ways to develop agents:  

## 1. Low/No Code UI  
<img width="800" alt="UI Example" src="https://github.com/user-attachments/assets/a7c57c50-1df9-4c37-be3d-0d2cedfaabfe" />  

### Pros
- Easy to use, with side-by-side editing and testing.

### Cons
1. Limited functionality:
   - Cannot call other agents within the same project.
   - Supports custom tools and can call tools in a custom agent.
2. Error messages are not intuitive:
   - Custom tools must include docstrings in the correct position with proper spacing, or they will result in a `400` error.
3. Examples screenshots:  
   <img width="500" height="500" alt="scorer" src="https://github.com/user-attachments/assets/554a074e-4c50-46d3-895b-bbcedb77ea44" />
   <img width="500" height="500" alt="approver" src="https://github.com/user-attachments/assets/e0d5fe60-a17b-4fee-b960-6f03e679feb8" />  

## 2. Developer Version for Advanced Settings  
The developer version provides more advanced customization options for building agents.
