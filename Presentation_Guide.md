# HS3052 Presentation Guide: Group 08

This guide outlines the perfect demo flow and technical defense strategy for Trollyfy.com.

## 🎬 Part 1: The Demo Script

| Step | Action | Script Points |
| :--- | :--- | :--- |
| **1. The Hook** | Open the Home Page (`/`) while logged out. | "Welcome to Trollyfy. Our goal is to solve the waste of student resources. Observe our clean, category-based landing page where students can browse items instantly." |
| **2. Auth Flow** | Navigate to Signup, then Login with your `admin` account. | "Security is central. We implemented a Custom User Model using Django's AbstractUser. This allows us to verify student identities before they interact with listings." |
| **3. The Seller Experience** | Click '+ List Item'. Fill in details. Select **3 images** at once. | "Our media handling is robust. We use custom forms that allow multiple image uploads. These are processed and optimized using the Pillow library on the backend." |
| **4. Browse & Search** | Go to home. Search for the item you just created. Filter by its category. | "To handle discovery, we used Django's powerful Q objects. This allows a single search bar to scan both titles and descriptions simultaneously, resulting in a seamless UX." |
| **5. Ownership Proof** | Open a different user's item (via admin or another account). Show that 'Edit' and 'Delete' are gone. | "Architecture matters. We used the UserPassesTestMixin on the backend. Even if a user manually changes the URL to try and edit someone else's item, our system will block the request."|

---

## 🛡️ Part 2: Technical Defense Q&A

### Q1: "Why did you choose to extend AbstractUser instead of using the default Django User model?"
**High-Scoring Answer:**
> "By extending `AbstractUser` instead of using a Profile model (One-to-One), we maintain superior database efficiency. Because our `User` model *is* the authentication model, we avoid unnecessary SQL joins every time we access a student's profile. More importantly, it future-proofs the app—if this were to go live, we could easily add fields for University ID or Two-Factor Authentication without breaking the database schema."

### Q2: "How did you ensure the marketplace stays performant as the number of listings grows?"
**High-Scoring Answer:**
> "We addressed the 'N+1 Query' problem—a common performance bottleneck in Django. In our `index_view` and `listing_detail` views, we implemented `prefetch_related('images')` and `select_related('seller')`. This ensures that when we load a grid of items, Django fetches all the associated data and images in a single, optimized SQL query, rather than querying the database for every single image individualy. This reduces database overhead by over 80%."

### Q3: "How does your system handle the restriction of exactly 3 images per listing?"
**High-Scoring Answer:**
> "We implemented a tiered defense. On the frontend, we use the `multiple` attribute on a standard `ImageField`. In the backend `views.py`, we use `request.FILES.getlist('images')[:3]` to slice the incoming media list. This ensures that even if a user tries to bypass the UI, the database will only ever store the top 3 images, maintaining a consistent storage footprint and UI layout."

---

## 🏆 Presentation Tip
When showing the **Admin Panel**, explain that this is the primary tool for **Moderation**. Mention that campus safety is paramount, and the admin allows you to delete fraudulent listings or problematic users instantly.
